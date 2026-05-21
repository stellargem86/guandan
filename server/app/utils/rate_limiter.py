"""API 限流中间件 - IP + User ID 双重限流

基于 Redis 滑动窗口计数器实现，支持：
- IP 限流：防止单 IP 滥用
- User ID 限流：防止单用户高频访问
- 可配置每端点的限流阈值
- 超限返回 429 Too Many Requests
"""

import time
from typing import Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from app.core.redis import redis_manager


class RateLimitConfig:
    """限流配置"""

    def __init__(
        self,
        default_max_requests: int = 60,
        default_window_seconds: int = 60,
        endpoint_limits: Optional[dict[str, tuple[int, int]]] = None,
    ):
        """
        Args:
            default_max_requests: 默认每窗口最大请求数
            default_window_seconds: 默认窗口时长 (秒)
            endpoint_limits: 端点自定义限制 {path: (max_requests, window_seconds)}
        """
        self.default_max_requests = default_max_requests
        self.default_window_seconds = default_window_seconds
        self.endpoint_limits = endpoint_limits or {}


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """IP + User ID 双重限流中间件"""

    def __init__(self, app, config: Optional[RateLimitConfig] = None):
        super().__init__(app)
        self.config = config or RateLimitConfig()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # 跳过健康检查和文档端点
        if request.url.path in ("/health", "/docs", "/redoc", "/openapi.json"):
            return await call_next(request)

        # 获取端点限流配置
        endpoint = request.url.path
        max_requests, window_seconds = self.config.endpoint_limits.get(
            endpoint, (self.config.default_max_requests, self.config.default_window_seconds)
        )

        # 获取客户端 IP
        client_ip = self._get_client_ip(request)

        # 获取用户 ID (从请求 state 或 header 中)
        user_id = self._get_user_id(request)

        try:
            # IP 限流检查
            ip_allowed, ip_remaining = await redis_manager.check_rate_limit(
                identifier=client_ip,
                endpoint=endpoint,
                max_requests=max_requests,
                window_seconds=window_seconds,
            )

            if not ip_allowed:
                ttl = await redis_manager.get_rate_limit_ttl(client_ip, endpoint)
                return self._rate_limit_response(ttl, max_requests)

            # User ID 限流检查（如果用户已登录）
            user_remaining = max_requests
            if user_id:
                user_allowed, user_remaining = await redis_manager.check_rate_limit(
                    identifier=f"user:{user_id}",
                    endpoint=endpoint,
                    max_requests=max_requests,
                    window_seconds=window_seconds,
                )
                if not user_allowed:
                    ttl = await redis_manager.get_rate_limit_ttl(
                        f"user:{user_id}", endpoint
                    )
                    return self._rate_limit_response(ttl, max_requests)

            # 请求通过，添加限流响应头
            response = await call_next(request)
            remaining = min(ip_remaining, user_remaining)
            response.headers["X-RateLimit-Limit"] = str(max_requests)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Window"] = str(window_seconds)
            return response

        except RuntimeError:
            # Redis 未连接时放行请求（降级策略）
            return await call_next(request)

    def _get_client_ip(self, request: Request) -> str:
        """获取客户端真实 IP（支持代理转发）"""
        # 优先从 X-Forwarded-For 获取
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()

        # 直连 IP
        if request.client:
            return request.client.host
        return "unknown"

    def _get_user_id(self, request: Request) -> Optional[str]:
        """从请求中提取用户 ID

        尝试从 Authorization header 解析 JWT 获取用户 ID。
        这里做简单提取，完整的 JWT 验证由认证中间件处理。
        """
        # 从请求 state 中获取（认证中间件设置的）
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return str(user_id)
        return None

    def _rate_limit_response(self, retry_after: int, limit: int) -> JSONResponse:
        """生成 429 限流响应"""
        return JSONResponse(
            status_code=429,
            content={
                "detail": "请求过于频繁，请稍后再试",
                "code": "RATE_LIMIT_EXCEEDED",
                "retry_after": max(retry_after, 1),
            },
            headers={
                "Retry-After": str(max(retry_after, 1)),
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
            },
        )

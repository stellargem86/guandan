"""FastAPI 应用入口 - 初始化应用、中间件、路由"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.redis import redis_manager
from app.utils.rate_limiter import RateLimiterMiddleware, RateLimitConfig
from app.api.v1 import auth, posts, merchants, matchmaking, events, clubs, rankings, orders, wallet, admin, articles, ads, users

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理 - 启动/关闭时初始化/释放资源"""
    # Startup: 尝试初始化 Redis 连接（开发环境可能没有 Redis）
    try:
        await redis_manager.connect()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Redis 连接失败（开发模式继续运行）: {e}")
    yield
    # Shutdown: 关闭 Redis 连接
    try:
        await redis_manager.disconnect()
    except Exception:
        pass


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# 限流中间件（在 CORS 之前添加）
rate_limit_config = RateLimitConfig(
    default_max_requests=60,
    default_window_seconds=60,
    endpoint_limits={
        # 认证接口更严格限流
        "/api/v1/auth/wechat-login": (10, 60),
        "/api/v1/auth/refresh-token": (20, 60),
        # 支付相关接口
        "/api/v1/orders": (30, 60),
    },
)
app.add_middleware(RateLimiterMiddleware, config=rate_limit_config)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 v1 路由
app.include_router(auth.router, prefix=settings.API_V1_PREFIX + "/auth", tags=["认证"])
app.include_router(posts.router, prefix=settings.API_V1_PREFIX + "/posts", tags=["掼友圈"])
app.include_router(merchants.router, prefix=settings.API_V1_PREFIX + "/merchants", tags=["商户"])
app.include_router(matchmaking.router, prefix=settings.API_V1_PREFIX + "/matchmaking", tags=["组局"])
app.include_router(events.router, prefix=settings.API_V1_PREFIX + "/events", tags=["赛事"])
app.include_router(clubs.router, prefix=settings.API_V1_PREFIX + "/clubs", tags=["俱乐部"])
app.include_router(rankings.router, prefix=settings.API_V1_PREFIX + "/rankings", tags=["排行榜"])
app.include_router(orders.router, prefix=settings.API_V1_PREFIX + "/orders", tags=["订单"])
app.include_router(wallet.router, prefix=settings.API_V1_PREFIX + "/wallet", tags=["钱包"])
app.include_router(articles.router, prefix=settings.API_V1_PREFIX + "/articles", tags=["资讯"])
app.include_router(ads.router, prefix=settings.API_V1_PREFIX + "/ads", tags=["广告"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX + "/users", tags=["用户"])
app.include_router(admin.router, prefix=settings.API_V1_PREFIX + "/admin", tags=["管理"])


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok", "version": settings.APP_VERSION}

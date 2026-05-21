"""路由级公共依赖 - JWT 认证、RBAC 权限检查

角色层级：
- user: 基础用户（所有已认证用户）
- merchant: 商户（可访问商户相关接口）
- organizer: 组织者（可管理赛事和俱乐部）
- admin: 超级管理员（可访问所有接口）

权限规则：
- Admin 可访问所有接口
- Merchant/Organizer 是平行的角色，各自有独立的接口权限
- User 只能访问基础用户接口
"""

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token, is_token_blacklisted
from app.models.user import User

security_scheme = HTTPBearer()

# 角色层级定义（admin 拥有最高权限，可访问所有资源）
ROLE_HIERARCHY = {
    "user": 0,
    "merchant": 1,
    "organizer": 1,
    "admin": 2,
}


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """解析 JWT Token 获取当前用户

    从 Authorization: Bearer <token> 提取 token，解码验证后查询用户。

    Returns:
        当前认证用户的 User ORM 对象

    Raises:
        HTTPException 401: Token 无效、过期、被撤销或用户不存在
        HTTPException 403: 用户账号被封禁
    """
    token = credentials.credentials

    # 解码 Token
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证 Token 类型
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 Token 类型",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查 Token 黑名单
    jti = payload.get("jti")
    if jti and await is_token_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 已被撤销",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 获取用户 ID
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 Token 内容",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 查询用户
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查用户状态
    if user.status == "banned":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被封禁",
        )

    return user


class RoleChecker:
    """RBAC 角色检查器

    支持多角色校验，Admin 自动拥有所有权限。

    Usage:
        require_admin = RoleChecker(["admin"])
        require_merchant = RoleChecker(["merchant", "admin"])
        require_organizer = RoleChecker(["organizer", "admin"])

        @router.get("/admin-only")
        async def admin_endpoint(user: User = Depends(require_admin)):
            ...
    """

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self, current_user: User = Depends(get_current_user)
    ) -> User:
        """验证当前用户是否拥有所需角色

        Args:
            current_user: 通过 get_current_user 依赖注入的用户

        Returns:
            验证通过的用户对象

        Raises:
            HTTPException 403: 权限不足
        """
        # Admin 拥有所有权限
        if current_user.role == "admin":
            return current_user

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"权限不足，需要以下角色之一: {', '.join(self.allowed_roles)}",
            )

        return current_user


def require_role(*roles: str) -> Callable:
    """角色要求工厂函数

    创建一个 FastAPI 依赖，要求当前用户拥有指定角色之一。
    Admin 角色自动拥有所有权限。

    Args:
        *roles: 允许的角色列表

    Returns:
        FastAPI 依赖函数

    Usage:
        @router.get("/merchant-data")
        async def merchant_data(user: User = Depends(require_role("merchant", "admin"))):
            ...
    """
    checker = RoleChecker(list(roles))
    return checker


# ─── 预置角色依赖 ─────────────────────────────────────────────────

# Admin 权限：仅超级管理员可访问
require_admin = RoleChecker(["admin"])

# 商户权限：商户和管理员可访问
require_merchant = RoleChecker(["merchant", "admin"])
require_merchant_or_admin = require_merchant  # 别名，语义更清晰

# 组织者权限：组织者和管理员可访问
require_organizer = RoleChecker(["organizer", "admin"])
require_organizer_or_admin = require_organizer  # 别名，语义更清晰

# 任意已认证用户（直接使用 get_current_user 依赖即可）

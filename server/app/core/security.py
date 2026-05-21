"""JWT 认证工具 - Token 签发、验证、密码哈希、Token 黑名单"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from uuid import uuid4

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import get_settings

settings = get_settings()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)

# Token 黑名单 Redis key 前缀
TOKEN_BLACKLIST_PREFIX = "token:blacklist:"


def create_access_token(
    user_id: str | int,
    role: str = "user",
    expires_delta: timedelta | None = None,
) -> str:
    """创建 Access Token

    Payload: {"sub": user_id, "role": role, "type": "access", "exp": ..., "jti": ...}

    Args:
        user_id: 用户 ID
        role: 用户角色 (user/merchant/organizer/admin)
        expires_delta: 自定义过期时间，默认使用配置值

    Returns:
        编码后的 JWT 字符串
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": expire,
        "jti": uuid4().hex,  # JWT ID，用于黑名单
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(
    user_id: str | int,
    expires_delta: timedelta | None = None,
) -> str:
    """创建 Refresh Token

    Payload: {"sub": user_id, "type": "refresh", "exp": ..., "jti": ...}

    Args:
        user_id: 用户 ID
        expires_delta: 自定义过期时间，默认使用配置值

    Returns:
        编码后的 JWT 字符串
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
        "jti": uuid4().hex,
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """解码并验证 Token

    Args:
        token: JWT 字符串

    Returns:
        解码后的 payload 字典，验证失败返回 None
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def generate_platform_id() -> str:
    """生成平台唯一用户 ID

    Returns:
        16 位十六进制字符串
    """
    return uuid4().hex[:16]


# ─── Token 黑名单操作（通过 Redis）─────────────────────────────────


async def add_token_to_blacklist(
    jti: str, expires_in_seconds: int
) -> None:
    """将 Token 加入黑名单（用于登出/Token 撤销）"""
    from app.core.redis import redis_manager

    if not redis_manager.is_connected:
        return
    try:
        key = f"{TOKEN_BLACKLIST_PREFIX}{jti}"
        await redis_manager.client.set(key, "1", ex=expires_in_seconds)
    except Exception:
        pass


async def is_token_blacklisted(jti: str) -> bool:
    """检查 Token 是否在黑名单中"""
    from app.core.redis import redis_manager

    if not redis_manager.is_connected:
        return False
    try:
        key = f"{TOKEN_BLACKLIST_PREFIX}{jti}"
        result = await redis_manager.client.get(key)
        return result is not None
    except Exception:
        return False

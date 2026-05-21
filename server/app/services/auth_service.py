"""认证服务 - 微信登录、Token 刷新、用户查询

提供微信 OAuth 2.0 登录流程：
1. 接收前端传来的 wx.login() code
2. 调用微信 code2session 获取 openid
3. 查找或创建用户
4. 签发 Access + Refresh Token
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_platform_id,
    is_token_blacklisted,
    add_token_to_blacklist,
)
from app.core.wechat import wechat_sdk, WeChatError
from app.models.user import User


class AuthServiceError(Exception):
    """认证服务异常"""

    def __init__(self, message: str, code: str = "AUTH_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


async def wechat_login(code: str, db: AsyncSession) -> dict:
    """微信登录流程

    通过微信 code 换取 openid，查找或创建用户，签发 JWT Token。

    Args:
        code: 微信小程序前端 wx.login() 获取的临时登录凭证
        db: 数据库 Session

    Returns:
        {
            "access_token": str,
            "refresh_token": str,
            "token_type": "bearer",
            "user": User ORM 对象
        }

    Raises:
        AuthServiceError: 微信 API 调用失败或其他认证错误
    """
    # 1. 调用微信 code2session 获取 openid
    try:
        session_data = await wechat_sdk.code2session(code)
    except WeChatError as e:
        raise AuthServiceError(
            message=f"微信登录失败: {e.errmsg}",
            code="WECHAT_LOGIN_FAILED",
        )

    openid = session_data["openid"]
    unionid = session_data.get("unionid")

    # 2. 根据 openid 查找已有用户
    result = await db.execute(
        select(User).where(User.wechat_openid == openid)
    )
    user = result.scalar_one_or_none()

    # 3. 如果用户不存在，创建新用户
    if user is None:
        user = User(
            platform_id=generate_platform_id(),
            wechat_openid=openid,
            wechat_unionid=unionid,
            nickname=f"掼友_{openid[-6:]}",  # 默认昵称
            role="user",
            status="active",
        )
        db.add(user)
        await db.flush()  # 获取 user.id
    else:
        # 更新 unionid（如果之前没有）
        if unionid and not user.wechat_unionid:
            user.wechat_unionid = unionid
            await db.flush()

    # 4. 签发 Token
    access_token = create_access_token(user_id=user.id, role=user.role)
    refresh_token = create_refresh_token(user_id=user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user,
    }


async def refresh_tokens(refresh_token: str, db: AsyncSession) -> dict:
    """刷新 Token

    验证 Refresh Token 有效性，签发新的 Access + Refresh Token。
    旧的 Refresh Token 加入黑名单（单次使用）。

    Args:
        refresh_token: 当前的 Refresh Token
        db: 数据库 Session

    Returns:
        {
            "access_token": str,
            "refresh_token": str,
            "token_type": "bearer"
        }

    Raises:
        AuthServiceError: Token 无效、过期或已被撤销
    """
    # 1. 解码 Refresh Token
    payload = decode_token(refresh_token)
    if payload is None:
        raise AuthServiceError(
            message="无效的 Refresh Token",
            code="INVALID_REFRESH_TOKEN",
        )

    # 2. 验证 Token 类型
    if payload.get("type") != "refresh":
        raise AuthServiceError(
            message="Token 类型错误",
            code="INVALID_TOKEN_TYPE",
        )

    # 3. 检查黑名单
    jti = payload.get("jti")
    if jti and await is_token_blacklisted(jti):
        raise AuthServiceError(
            message="Refresh Token 已被撤销",
            code="TOKEN_REVOKED",
        )

    # 4. 查询用户
    user_id = payload.get("sub")
    if user_id is None:
        raise AuthServiceError(
            message="无效的 Token 内容",
            code="INVALID_TOKEN_PAYLOAD",
        )

    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise AuthServiceError(
            message="用户不存在",
            code="USER_NOT_FOUND",
        )

    if user.status == "banned":
        raise AuthServiceError(
            message="账号已被封禁",
            code="USER_BANNED",
        )

    # 5. 将旧 Refresh Token 加入黑名单
    if jti:
        # 计算剩余有效期（秒）
        import time

        exp = payload.get("exp", 0)
        remaining = max(int(exp - time.time()), 0)
        if remaining > 0:
            await add_token_to_blacklist(jti, remaining)

    # 6. 签发新 Token
    new_access_token = create_access_token(user_id=user.id, role=user.role)
    new_refresh_token = create_refresh_token(user_id=user.id)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }

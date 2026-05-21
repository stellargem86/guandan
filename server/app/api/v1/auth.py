"""认证路由 - 微信登录、Token 刷新、用户信息

提供以下接口：
- POST /wechat-login: 微信小程序授权登录
- POST /refresh-token: 刷新 JWT Token
- GET /me: 获取当前用户信息（需认证）
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    WeChatLoginRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthServiceError, refresh_tokens, wechat_login

router = APIRouter()


@router.post("/wechat-login", response_model=LoginResponse)
async def wechat_login_endpoint(
    body: WeChatLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """微信授权登录

    接收微信小程序前端 wx.login() 获取的临时 code，
    调用微信 code2session 换取 openid，查找或创建用户，返回 JWT Token。

    Returns:
        LoginResponse: 包含 access_token, refresh_token, token_type, user
    """
    try:
        result = await wechat_login(code=body.code, db=db)
    except AuthServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )

    return LoginResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"],
        user=UserResponse.model_validate(result["user"]),
    )


@router.post("/refresh-token", response_model=RefreshTokenResponse)
async def refresh_token_endpoint(
    body: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """刷新 JWT Token

    使用 Refresh Token 获取新的 Access + Refresh Token 对。
    旧的 Refresh Token 使用后即失效（单次使用机制）。

    Returns:
        RefreshTokenResponse: 包含新的 access_token, refresh_token, token_type
    """
    try:
        result = await refresh_tokens(
            refresh_token=body.refresh_token, db=db
        )
    except AuthServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )

    return RefreshTokenResponse(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
        token_type=result["token_type"],
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """获取当前用户信息

    需要有效的 Access Token（Authorization: Bearer <token>）。

    Returns:
        UserResponse: 当前认证用户的详细信息
    """
    return UserResponse.model_validate(current_user)

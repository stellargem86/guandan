"""认证相关 Pydantic Schemas

包含微信登录请求/响应、Token 刷新请求/响应等模式。
"""

from pydantic import BaseModel, Field

from app.schemas.user import UserResponse


class WeChatLoginRequest(BaseModel):
    """微信登录请求"""

    code: str = Field(..., description="微信小程序 wx.login() 获取的临时登录凭证")


class TokenResponse(BaseModel):
    """Token 响应"""

    access_token: str = Field(..., description="JWT Access Token")
    refresh_token: str = Field(..., description="JWT Refresh Token")
    token_type: str = Field(default="bearer", description="Token 类型")


class LoginResponse(TokenResponse):
    """登录响应（包含用户信息）"""

    user: UserResponse = Field(..., description="用户信息")


class RefreshTokenRequest(BaseModel):
    """刷新 Token 请求"""

    refresh_token: str = Field(..., description="Refresh Token")


class RefreshTokenResponse(TokenResponse):
    """刷新 Token 响应"""

    pass

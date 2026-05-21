"""用户 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """用户基础字段"""

    nickname: str = Field(..., max_length=64, description="用户昵称")
    avatar_url: str | None = Field(None, max_length=512, description="头像 URL")
    phone: str | None = Field(None, max_length=20, description="手机号")
    industry: str | None = Field(None, max_length=64, description="所属行业")


class UserCreate(UserBase):
    """创建用户"""

    platform_id: str = Field(..., max_length=32, description="平台唯一 ID")
    wechat_openid: str | None = Field(None, max_length=128, description="微信 OpenID")
    wechat_unionid: str | None = Field(None, max_length=128, description="微信 UnionID")


class UserUpdate(BaseModel):
    """更新用户（所有字段可选）"""

    nickname: str | None = Field(None, max_length=64)
    avatar_url: str | None = Field(None, max_length=512)
    phone: str | None = Field(None, max_length=20)
    industry: str | None = Field(None, max_length=64)
    role: str | None = Field(None, max_length=20)
    status: str | None = Field(None, max_length=20)


class UserInDB(UserBase):
    """数据库中的用户"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    platform_id: str
    wechat_openid: str | None = None
    wechat_unionid: str | None = None
    role: str = "user"
    status: str = "active"
    created_at: datetime
    updated_at: datetime


class UserResponse(UserInDB):
    """用户 API 响应"""

    pass

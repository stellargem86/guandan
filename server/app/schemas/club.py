"""俱乐部 & 成员 & 活动 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Club Schemas
# ============================================================


class ClubBase(BaseModel):
    """俱乐部基础字段"""

    name: str = Field(..., max_length=128, description="俱乐部名称")
    description: str | None = Field(None, description="俱乐部描述")
    avatar_url: str | None = Field(None, max_length=512, description="俱乐部头像")
    region: str | None = Field(None, max_length=64, description="所在地区")
    membership_fee: Decimal = Field(default=Decimal("0.00"), description="会员费")
    max_members: int = Field(default=200, description="最大成员数")


class ClubCreate(ClubBase):
    """创建俱乐部"""

    owner_id: int = Field(..., description="创建者用户ID")


class ClubUpdate(BaseModel):
    """更新俱乐部（所有字段可选）"""

    name: str | None = Field(None, max_length=128)
    description: str | None = None
    avatar_url: str | None = Field(None, max_length=512)
    region: str | None = Field(None, max_length=64)
    membership_fee: Decimal | None = None
    max_members: int | None = None
    status: str | None = Field(None, max_length=20)


class ClubInDB(ClubBase):
    """数据库中的俱乐部"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    current_members: int = 1
    status: str = "active"
    created_at: datetime
    updated_at: datetime


class ClubResponse(ClubInDB):
    """俱乐部 API 响应"""

    pass


# ============================================================
# ClubMember Schemas
# ============================================================


class ClubMemberBase(BaseModel):
    """俱乐部成员基础字段"""

    club_id: int = Field(..., description="所属俱乐部ID")
    user_id: int = Field(..., description="成员用户ID")


class ClubMemberCreate(ClubMemberBase):
    """创建俱乐部成员"""

    role: str = Field(default="member", max_length=20, description="角色")
    order_id: int | None = Field(None, description="关联订单ID（会员费）")


class ClubMemberUpdate(BaseModel):
    """更新俱乐部成员（所有字段可选）"""

    role: str | None = Field(None, max_length=20)
    status: str | None = Field(None, max_length=20)


class ClubMemberInDB(ClubMemberBase):
    """数据库中的俱乐部成员"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str = "member"
    order_id: int | None = None
    joined_at: datetime
    status: str = "active"


class ClubMemberResponse(ClubMemberInDB):
    """俱乐部成员 API 响应"""

    pass


# ============================================================
# ClubActivity Schemas
# ============================================================


class ClubActivityBase(BaseModel):
    """俱乐部活动基础字段"""

    title: str = Field(..., max_length=128, description="活动标题")
    description: str | None = Field(None, description="活动描述")
    activity_time: datetime | None = Field(None, description="活动时间")
    location: str | None = Field(None, max_length=256, description="活动地点")


class ClubActivityCreate(ClubActivityBase):
    """创建俱乐部活动"""

    club_id: int = Field(..., description="所属俱乐部ID")
    creator_id: int = Field(..., description="创建者用户ID")


class ClubActivityUpdate(BaseModel):
    """更新俱乐部活动（所有字段可选）"""

    title: str | None = Field(None, max_length=128)
    description: str | None = None
    activity_time: datetime | None = None
    location: str | None = Field(None, max_length=256)
    status: str | None = Field(None, max_length=20)


class ClubActivityInDB(ClubActivityBase):
    """数据库中的俱乐部活动"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    club_id: int
    creator_id: int
    status: str = "upcoming"
    created_at: datetime


class ClubActivityResponse(ClubActivityInDB):
    """俱乐部活动 API 响应"""

    pass

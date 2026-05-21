"""赛事 & 报名 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Event Schemas
# ============================================================


class EventBase(BaseModel):
    """赛事基础字段"""

    title: str = Field(..., max_length=128, description="赛事标题")
    description: str | None = Field(None, description="赛事描述")
    cover_image: str | None = Field(None, max_length=512, description="封面图片")
    event_date: datetime = Field(..., description="赛事日期")
    location: str | None = Field(None, max_length=256, description="赛事地点")
    entry_fee: Decimal = Field(default=Decimal("0.00"), description="报名费")
    max_capacity: int = Field(default=100, description="最大参赛人数")
    rules: str | None = Field(None, description="赛事规则")
    cancel_deadline: datetime | None = Field(None, description="取消报名截止时间")


class EventCreate(EventBase):
    """创建赛事"""

    organizer_id: int = Field(..., description="组织者用户ID")


class EventUpdate(BaseModel):
    """更新赛事（所有字段可选）"""

    title: str | None = Field(None, max_length=128)
    description: str | None = None
    cover_image: str | None = Field(None, max_length=512)
    event_date: datetime | None = None
    location: str | None = Field(None, max_length=256)
    entry_fee: Decimal | None = None
    max_capacity: int | None = None
    rules: str | None = None
    cancel_deadline: datetime | None = None
    status: str | None = Field(None, max_length=20)


class EventInDB(EventBase):
    """数据库中的赛事"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    organizer_id: int
    current_registrations: int = 0
    status: str = "upcoming"
    created_at: datetime
    updated_at: datetime


class EventResponse(EventInDB):
    """赛事 API 响应"""

    pass


# ============================================================
# EventRegistration Schemas
# ============================================================


class EventRegistrationBase(BaseModel):
    """赛事报名基础字段"""

    event_id: int = Field(..., description="关联赛事ID")
    user_id: int = Field(..., description="报名用户ID")


class EventRegistrationCreate(EventRegistrationBase):
    """创建赛事报名"""

    order_id: int | None = Field(None, description="关联订单ID")


class EventRegistrationUpdate(BaseModel):
    """更新赛事报名（所有字段可选）"""

    status: str | None = Field(None, max_length=20)
    checked_in_at: datetime | None = None


class EventRegistrationInDB(EventRegistrationBase):
    """数据库中的赛事报名"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int | None = None
    status: str = "registered"
    checked_in_at: datetime | None = None
    created_at: datetime


class EventRegistrationResponse(EventRegistrationInDB):
    """赛事报名 API 响应"""

    pass

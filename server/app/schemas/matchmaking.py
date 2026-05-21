"""组局 & 参与者 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# MatchmakingRequest Schemas
# ============================================================


class MatchmakingRequestBase(BaseModel):
    """组局请求基础字段"""

    title: str = Field(..., max_length=128, description="组局标题")
    scheduled_time: datetime = Field(..., description="预定时间")
    location: str | None = Field(None, max_length=256, description="地点")
    latitude: Decimal | None = Field(None, description="纬度")
    longitude: Decimal | None = Field(None, description="经度")
    min_rank: str | None = Field(None, max_length=20, description="最低段位要求")
    max_rank: str | None = Field(None, max_length=20, description="最高段位要求")
    industry_tag: str | None = Field(None, max_length=64, description="行业标签")
    max_players: int = Field(default=4, description="最大人数")
    deposit_amount: Decimal = Field(default=Decimal("0.00"), description="押金金额")


class MatchmakingRequestCreate(MatchmakingRequestBase):
    """创建组局请求"""

    creator_id: int = Field(..., description="创建者用户ID")


class MatchmakingRequestUpdate(BaseModel):
    """更新组局请求（所有字段可选）"""

    title: str | None = Field(None, max_length=128)
    scheduled_time: datetime | None = None
    location: str | None = Field(None, max_length=256)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    min_rank: str | None = Field(None, max_length=20)
    max_rank: str | None = Field(None, max_length=20)
    industry_tag: str | None = Field(None, max_length=64)
    max_players: int | None = None
    deposit_amount: Decimal | None = None
    status: str | None = Field(None, max_length=20)


class MatchmakingRequestInDB(MatchmakingRequestBase):
    """数据库中的组局请求"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    current_players: int = 1
    status: str = "open"
    created_at: datetime
    updated_at: datetime


class MatchmakingRequestResponse(MatchmakingRequestInDB):
    """组局请求 API 响应"""

    pass


# ============================================================
# MatchmakingParticipant Schemas
# ============================================================


class MatchmakingParticipantBase(BaseModel):
    """组局参与者基础字段"""

    request_id: int = Field(..., description="关联组局请求ID")
    user_id: int = Field(..., description="参与者用户ID")


class MatchmakingParticipantCreate(MatchmakingParticipantBase):
    """创建组局参与者"""

    deposit_order_id: int | None = Field(None, description="押金订单ID")


class MatchmakingParticipantUpdate(BaseModel):
    """更新组局参与者（所有字段可选）"""

    status: str | None = Field(None, max_length=20)
    cancelled_at: datetime | None = None


class MatchmakingParticipantInDB(MatchmakingParticipantBase):
    """数据库中的组局参与者"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str = "joined"
    deposit_order_id: int | None = None
    joined_at: datetime
    cancelled_at: datetime | None = None


class MatchmakingParticipantResponse(MatchmakingParticipantInDB):
    """组局参与者 API 响应"""

    pass

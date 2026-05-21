"""ELO 积分 & 对局记录 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# EloScore Schemas
# ============================================================


class EloScoreBase(BaseModel):
    """ELO 积分基础字段"""

    user_id: int = Field(..., description="所属用户ID")


class EloScoreCreate(EloScoreBase):
    """创建 ELO 积分记录"""

    score: int = Field(default=1200, description="初始 ELO 分")
    region: str | None = Field(None, max_length=64, description="地区")


class EloScoreUpdate(BaseModel):
    """更新 ELO 积分（所有字段可选）"""

    score: int | None = None
    tier: str | None = Field(None, max_length=20)
    total_matches: int | None = None
    wins: int | None = None
    losses: int | None = None
    win_rate: Decimal | None = None
    k_factor: int | None = None
    region: str | None = Field(None, max_length=64)


class EloScoreInDB(EloScoreBase):
    """数据库中的 ELO 积分"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    score: int = 1200
    tier: str = "bronze"
    total_matches: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: Decimal = Decimal("0.0000")
    k_factor: int = 32
    region: str | None = None
    updated_at: datetime


class EloScoreResponse(EloScoreInDB):
    """ELO 积分 API 响应"""

    pass


# ============================================================
# MatchResult Schemas
# ============================================================


class MatchResultBase(BaseModel):
    """对局记录基础字段"""

    winner_id: int = Field(..., description="胜者用户ID")
    loser_id: int = Field(..., description="败者用户ID")
    winner_score_before: int = Field(..., description="胜者赛前分数")
    winner_score_after: int = Field(..., description="胜者赛后分数")
    loser_score_before: int = Field(..., description="败者赛前分数")
    loser_score_after: int = Field(..., description="败者赛后分数")


class MatchResultCreate(MatchResultBase):
    """创建对局记录"""

    event_id: int | None = Field(None, description="关联赛事ID")
    recorded_by: int | None = Field(None, description="记录者用户ID")


class MatchResultUpdate(BaseModel):
    """更新对局记录（所有字段可选）"""

    event_id: int | None = None
    recorded_by: int | None = None


class MatchResultInDB(MatchResultBase):
    """数据库中的对局记录"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int | None = None
    recorded_by: int | None = None
    created_at: datetime


class MatchResultResponse(MatchResultInDB):
    """对局记录 API 响应"""

    pass

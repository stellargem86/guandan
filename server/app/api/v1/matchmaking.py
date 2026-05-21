"""一键组局路由

提供以下接口：
- POST /matchmaking: 创建组局
- GET /matchmaking: 获取组局列表（支持筛选）
- POST /matchmaking/:id/join: 加入组局
- POST /matchmaking/:id/cancel: 取消参加
"""

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.matchmaking import (
    MatchmakingParticipantResponse,
    MatchmakingRequestResponse,
)
from app.services import matchmaking_service

router = APIRouter()


# ─── Request Schemas ─────────────────────────────────────────────


class CreateMatchmakingBody(BaseModel):
    """创建组局请求体"""

    title: str = Field(..., max_length=128, description="组局标题")
    scheduled_time: datetime = Field(..., description="预定时间")
    location: str | None = Field(None, max_length=256, description="地点")
    latitude: float | None = Field(None, description="纬度")
    longitude: float | None = Field(None, description="经度")
    min_rank: str | None = Field(None, max_length=20, description="最低段位要求")
    max_rank: str | None = Field(None, max_length=20, description="最高段位要求")
    industry_tag: str | None = Field(None, max_length=64, description="行业标签")
    max_players: int = Field(default=4, ge=2, le=20, description="最大人数")
    deposit_amount: Decimal = Field(default=Decimal("0.00"), ge=0, description="押金金额")


# ─── Endpoints ───────────────────────────────────────────────────


@router.post("", response_model=MatchmakingRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_matchmaking(
    body: CreateMatchmakingBody,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建组局

    需要认证。创建者自动加入为参与者。
    """
    result = await matchmaking_service.create_matchmaking(
        creator_id=current_user.id,
        title=body.title,
        scheduled_time=body.scheduled_time,
        location=body.location,
        latitude=body.latitude,
        longitude=body.longitude,
        min_rank=body.min_rank,
        max_rank=body.max_rank,
        industry_tag=body.industry_tag,
        max_players=body.max_players,
        deposit_amount=float(body.deposit_amount),
        db=db,
    )
    return MatchmakingRequestResponse.model_validate(result)


@router.get("")
async def list_matchmaking(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    status_filter: str | None = Query(default=None, alias="status", description="状态筛选"),
    rank: str | None = Query(default=None, description="段位筛选"),
    industry: str | None = Query(default=None, description="行业筛选"),
    db: AsyncSession = Depends(get_db),
):
    """获取组局列表

    支持按状态、段位、行业筛选。
    """
    result = await matchmaking_service.get_matchmaking_list(
        page=page,
        page_size=page_size,
        status_filter=status_filter,
        rank_filter=rank,
        industry_filter=industry,
        db=db,
    )
    return {
        "items": [MatchmakingRequestResponse.model_validate(item) for item in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
    }


@router.post("/{match_id}/join", response_model=MatchmakingParticipantResponse)
async def join_matchmaking(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """加入组局

    需要认证。检查容量和去重。
    """
    try:
        participant = await matchmaking_service.join_matchmaking(
            request_id=match_id,
            user_id=current_user.id,
            db=db,
        )
        return MatchmakingParticipantResponse.model_validate(participant)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{match_id}/cancel")
async def cancel_matchmaking(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取消参加

    需要认证。距预定时间 < 2 小时扣押金，否则全额退还。
    """
    try:
        result = await matchmaking_service.cancel_participation(
            request_id=match_id,
            user_id=current_user.id,
            db=db,
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

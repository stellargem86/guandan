"""赛事路由

提供以下接口：
- GET /events: 赛事列表
- GET /events/:id: 赛事详情
- POST /events/:id/register: 赛事报名
- POST /events/:id/cancel: 取消报名
- POST /events/:id/checkin: 签到
- POST /events/:id/scores: 提交成绩（组织者专用）
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_organizer
from app.core.database import get_db
from app.models.user import User
from app.schemas.event import EventRegistrationResponse, EventResponse
from app.schemas.elo import MatchResultResponse
from app.services import event_service

router = APIRouter()


# ─── Request Schemas ─────────────────────────────────────────────


class ScoreItem(BaseModel):
    """单条成绩记录"""

    winner_id: int = Field(..., description="胜者用户ID")
    loser_id: int = Field(..., description="败者用户ID")


class SubmitScoresBody(BaseModel):
    """提交成绩请求体"""

    results: list[ScoreItem] = Field(..., min_length=1, description="对局结果列表")


# ─── Endpoints ───────────────────────────────────────────────────


@router.get("")
async def list_events(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    status_filter: str | None = Query(default=None, alias="status", description="状态筛选"),
    db: AsyncSession = Depends(get_db),
):
    """获取赛事列表"""
    result = await event_service.get_events(
        page=page,
        page_size=page_size,
        status_filter=status_filter,
        db=db,
    )
    return {
        "items": [EventResponse.model_validate(item) for item in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
    }


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取赛事详情"""
    event = await event_service.get_event_detail(event_id=event_id, db=db)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="赛事不存在",
        )
    return EventResponse.model_validate(event)


@router.post("/{event_id}/register", response_model=EventRegistrationResponse)
async def register_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """赛事报名

    需要认证。检查容量和去重。
    """
    try:
        registration = await event_service.register_event(
            event_id=event_id,
            user_id=current_user.id,
            db=db,
        )
        return EventRegistrationResponse.model_validate(registration)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{event_id}/cancel")
async def cancel_registration(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取消报名

    需要认证。检查截止时间。
    """
    try:
        await event_service.cancel_registration(
            event_id=event_id,
            user_id=current_user.id,
            db=db,
        )
        return {"success": True, "message": "已取消报名"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{event_id}/checkin", response_model=EventRegistrationResponse)
async def checkin_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """赛事签到

    需要认证。设置签到时间。
    """
    try:
        registration = await event_service.checkin(
            event_id=event_id,
            user_id=current_user.id,
            db=db,
        )
        return EventRegistrationResponse.model_validate(registration)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{event_id}/scores")
async def submit_scores(
    event_id: int,
    body: SubmitScoresBody,
    current_user: User = Depends(require_organizer),
    db: AsyncSession = Depends(get_db),
):
    """提交赛事成绩

    仅组织者可用。每对 winner/loser 自动更新 ELO 积分。
    """
    try:
        results = await event_service.submit_scores(
            event_id=event_id,
            results=[item.model_dump() for item in body.results],
            recorded_by=current_user.id,
            db=db,
        )
        return {
            "success": True,
            "results": [MatchResultResponse.model_validate(r) for r in results],
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

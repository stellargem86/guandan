"""俱乐部路由

提供以下接口：
- GET /clubs: 俱乐部列表
- POST /clubs: 创建俱乐部
- GET /clubs/:id: 俱乐部详情
- POST /clubs/:id/join: 加入俱乐部
- GET /clubs/:id/members: 成员列表
- POST /clubs/:id/activities: 创建活动
- GET /clubs/:id/activities: 活动列表
"""

from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.club import (
    ClubActivityResponse,
    ClubMemberResponse,
    ClubResponse,
)
from app.services import club_service

router = APIRouter()


# ─── Request Schemas ─────────────────────────────────────────────


class CreateClubBody(BaseModel):
    """创建俱乐部请求体"""

    name: str = Field(..., max_length=128, description="俱乐部名称")
    description: str | None = Field(None, description="俱乐部描述")
    region: str | None = Field(None, max_length=64, description="所在地区")
    membership_fee: Decimal = Field(default=Decimal("0.00"), ge=0, description="会员费")
    max_members: int = Field(default=200, ge=2, le=10000, description="最大成员数")


class CreateActivityBody(BaseModel):
    """创建俱乐部活动请求体"""

    title: str = Field(..., max_length=128, description="活动标题")
    description: str | None = Field(None, description="活动描述")
    activity_time: datetime | None = Field(None, description="活动时间")
    location: str | None = Field(None, max_length=256, description="活动地点")


# ─── Endpoints ───────────────────────────────────────────────────


@router.get("")
async def list_clubs(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    region: str | None = Query(default=None, description="地区筛选"),
    db: AsyncSession = Depends(get_db),
):
    """获取俱乐部列表"""
    result = await club_service.get_clubs(
        page=page,
        page_size=page_size,
        region_filter=region,
        db=db,
    )
    return {
        "items": [ClubResponse.model_validate(item) for item in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
    }


@router.post("", response_model=ClubResponse, status_code=status.HTTP_201_CREATED)
async def create_club(
    body: CreateClubBody,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建俱乐部

    需要认证。创建者自动成为 owner。
    """
    club = await club_service.create_club(
        owner_id=current_user.id,
        name=body.name,
        description=body.description,
        region=body.region,
        membership_fee=float(body.membership_fee),
        max_members=body.max_members,
        db=db,
    )
    return ClubResponse.model_validate(club)


@router.get("/{club_id}", response_model=ClubResponse)
async def get_club_detail(
    club_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取俱乐部详情"""
    club = await club_service.get_club_detail(club_id=club_id, db=db)
    if club is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="俱乐部不存在",
        )
    return ClubResponse.model_validate(club)


@router.post("/{club_id}/join", response_model=ClubMemberResponse)
async def join_club(
    club_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """加入俱乐部

    需要认证。检查容量和去重。
    """
    try:
        member = await club_service.join_club(
            club_id=club_id,
            user_id=current_user.id,
            db=db,
        )
        return ClubMemberResponse.model_validate(member)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{club_id}/members")
async def list_members(
    club_id: int,
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=50, ge=1, le=200, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """获取俱乐部成员列表"""
    result = await club_service.get_members(
        club_id=club_id,
        page=page,
        page_size=page_size,
        db=db,
    )
    return {
        "items": [ClubMemberResponse.model_validate(item) for item in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
    }


@router.post("/{club_id}/activities", response_model=ClubActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    club_id: int,
    body: CreateActivityBody,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建俱乐部活动

    需要认证。
    """
    try:
        activity = await club_service.create_activity(
            club_id=club_id,
            creator_id=current_user.id,
            title=body.title,
            description=body.description,
            activity_time=body.activity_time,
            location=body.location,
            db=db,
        )
        return ClubActivityResponse.model_validate(activity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{club_id}/activities")
async def list_activities(
    club_id: int,
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """获取俱乐部活动列表"""
    result = await club_service.get_activities(
        club_id=club_id,
        page=page,
        page_size=page_size,
        db=db,
    )
    return {
        "items": [ClubActivityResponse.model_validate(item) for item in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
    }

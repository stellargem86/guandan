"""排行榜路由

提供以下接口：
- GET /rankings/personal: 个人排行榜（Redis Sorted Set）
- GET /rankings/club: 俱乐部排行榜
- GET /rankings/regional: 地区排行榜
- GET /users/:id/elo: 用户 ELO 详情（数据库）
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis import redis_manager
from app.models.elo import EloScore
from app.schemas.elo import EloScoreResponse

router = APIRouter()


@router.get("/personal")
async def personal_ranking(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=50, ge=1, le=100, description="每页数量"),
):
    """个人排行榜

    从 Redis Sorted Set 获取 Top N 玩家排名。
    """
    start = (page - 1) * page_size
    end = start + page_size - 1

    rankings = await redis_manager.ranking_get_top(
        ranking_type="personal",
        start=start,
        end=end,
    )
    return {
        "items": rankings,
        "page": page,
        "page_size": page_size,
    }


@router.get("/club")
async def club_ranking(
    club_id: int = Query(..., description="俱乐部 ID"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=50, ge=1, le=100, description="每页数量"),
):
    """俱乐部排行榜

    获取指定俱乐部内成员的排名。
    """
    start = (page - 1) * page_size
    end = start + page_size - 1

    rankings = await redis_manager.ranking_get_top(
        ranking_type="club",
        start=start,
        end=end,
        ranking_id=str(club_id),
    )
    return {
        "items": rankings,
        "club_id": club_id,
        "page": page,
        "page_size": page_size,
    }


@router.get("/regional")
async def regional_ranking(
    region: str = Query(..., description="地区名称"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=50, ge=1, le=100, description="每页数量"),
):
    """地区排行榜

    获取指定地区玩家的排名。
    """
    start = (page - 1) * page_size
    end = start + page_size - 1

    rankings = await redis_manager.ranking_get_top(
        ranking_type="region",
        start=start,
        end=end,
        ranking_id=region,
    )
    return {
        "items": rankings,
        "region": region,
        "page": page,
        "page_size": page_size,
    }


@router.get("/users/{user_id}/elo", response_model=EloScoreResponse)
async def get_user_elo(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取用户 ELO 详情

    从数据库获取用户的完整 ELO 积分信息。
    """
    result = await db.execute(
        select(EloScore).where(EloScore.user_id == user_id)
    )
    elo = result.scalar_one_or_none()

    if elo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="该用户暂无 ELO 记录",
        )

    return EloScoreResponse.model_validate(elo)

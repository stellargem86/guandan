"""用户资料路由

提供以下接口：
- GET /users/me/profile: 获取个人资料（含 ELO 分数和徽章）
- PUT /users/me/profile: 更新个人资料（昵称、头像、行业）
"""

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.elo import EloScore
from app.models.user import User

router = APIRouter()


# ─── Response Schemas ────────────────────────────────────────────


class EloInfo(BaseModel):
    """ELO 积分摘要"""

    model_config = ConfigDict(from_attributes=True)

    score: int = 1200
    tier: str = "bronze"
    total_matches: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    rank: int | None = None


class BadgeInfo(BaseModel):
    """徽章信息"""

    id: str
    name: str
    icon: str
    earned_at: str | None = None


class UserProfileResponse(BaseModel):
    """用户个人资料响应"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    platform_id: str
    nickname: str
    avatar_url: str | None = None
    phone: str | None = None
    industry: str | None = None
    role: str = "user"
    status: str = "active"
    elo: EloInfo | None = None
    badges: list[BadgeInfo] = []


class UpdateProfileBody(BaseModel):
    """更新个人资料请求体"""

    nickname: str | None = Field(None, max_length=64, description="昵称")
    avatar_url: str | None = Field(None, max_length=512, description="头像 URL")
    industry: str | None = Field(None, max_length=64, description="行业")


# ─── Endpoints ───────────────────────────────────────────────────


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取个人资料

    返回用户基本信息、ELO 积分和徽章。
    """
    # 获取 ELO 积分
    elo_result = await db.execute(
        select(EloScore).where(EloScore.user_id == current_user.id)
    )
    elo_record = elo_result.scalar_one_or_none()

    elo_info = None
    if elo_record:
        from app.core.redis import redis_manager

        rank = await redis_manager.ranking_get_rank(
            ranking_type="personal",
            member=str(current_user.id),
        )
        elo_info = EloInfo(
            score=elo_record.score,
            tier=elo_record.tier,
            total_matches=elo_record.total_matches,
            wins=elo_record.wins,
            losses=elo_record.losses,
            win_rate=float(elo_record.win_rate),
            rank=rank + 1 if rank is not None else None,
        )

    # 徽章系统（简化版，基于成就）
    badges = _compute_badges(elo_record)

    return UserProfileResponse(
        id=current_user.id,
        platform_id=current_user.platform_id,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        phone=current_user.phone,
        industry=current_user.industry,
        role=current_user.role,
        status=current_user.status,
        elo=elo_info,
        badges=badges,
    )


@router.put("/me/profile", response_model=UserProfileResponse)
async def update_my_profile(
    body: UpdateProfileBody,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """更新个人资料

    可更新：昵称、头像、行业。
    """
    if body.nickname is not None:
        current_user.nickname = body.nickname
    if body.avatar_url is not None:
        current_user.avatar_url = body.avatar_url
    if body.industry is not None:
        current_user.industry = body.industry

    await db.commit()
    await db.refresh(current_user)

    # 获取 ELO 积分
    elo_result = await db.execute(
        select(EloScore).where(EloScore.user_id == current_user.id)
    )
    elo_record = elo_result.scalar_one_or_none()

    elo_info = None
    if elo_record:
        from app.core.redis import redis_manager

        rank = await redis_manager.ranking_get_rank(
            ranking_type="personal",
            member=str(current_user.id),
        )
        elo_info = EloInfo(
            score=elo_record.score,
            tier=elo_record.tier,
            total_matches=elo_record.total_matches,
            wins=elo_record.wins,
            losses=elo_record.losses,
            win_rate=float(elo_record.win_rate),
            rank=rank + 1 if rank is not None else None,
        )

    badges = _compute_badges(elo_record)

    return UserProfileResponse(
        id=current_user.id,
        platform_id=current_user.platform_id,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        phone=current_user.phone,
        industry=current_user.industry,
        role=current_user.role,
        status=current_user.status,
        elo=elo_info,
        badges=badges,
    )


def _compute_badges(elo_record: EloScore | None) -> list[BadgeInfo]:
    """根据 ELO 记录计算用户徽章

    简化版基于里程碑的徽章系统：
    - 初出茅庐：完成首场对局
    - 百战老将：完成 100 场对局
    - 常胜将军：胜率超过 60%
    - 段位徽章：根据段位颁发
    """
    badges = []

    if elo_record is None:
        return badges

    # 首场对局
    if elo_record.total_matches >= 1:
        badges.append(BadgeInfo(
            id="first_match",
            name="初出茅庐",
            icon="🎯",
        ))

    # 10 场对局
    if elo_record.total_matches >= 10:
        badges.append(BadgeInfo(
            id="ten_matches",
            name="小试牛刀",
            icon="⚔️",
        ))

    # 100 场对局
    if elo_record.total_matches >= 100:
        badges.append(BadgeInfo(
            id="hundred_matches",
            name="百战老将",
            icon="🏆",
        ))

    # 高胜率
    if elo_record.total_matches >= 10 and float(elo_record.win_rate) >= 0.6:
        badges.append(BadgeInfo(
            id="high_win_rate",
            name="常胜将军",
            icon="👑",
        ))

    # 段位徽章
    tier_badges = {
        "silver": BadgeInfo(id="tier_silver", name="白银段位", icon="🥈"),
        "gold": BadgeInfo(id="tier_gold", name="黄金段位", icon="🥇"),
        "platinum": BadgeInfo(id="tier_platinum", name="铂金段位", icon="💎"),
        "diamond": BadgeInfo(id="tier_diamond", name="钻石段位", icon="💠"),
    }
    if elo_record.tier in tier_badges:
        badges.append(tier_badges[elo_record.tier])

    return badges

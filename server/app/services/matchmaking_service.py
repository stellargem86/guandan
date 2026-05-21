"""组局匹配服务 - 创建组局、加入、取消参与

核心功能：
- create_matchmaking: 创建组局请求
- get_matchmaking_list: 分页获取组局列表（支持筛选）
- join_matchmaking: 加入组局（容量检查、去重）
- cancel_participation: 取消参加（押金逻辑：<2h 扣押金，否则退还）
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.matchmaking import MatchmakingParticipant, MatchmakingRequest


async def create_matchmaking(
    creator_id: int,
    title: str,
    scheduled_time: datetime,
    location: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    min_rank: str | None = None,
    max_rank: str | None = None,
    industry_tag: str | None = None,
    max_players: int = 4,
    deposit_amount: float = 0.00,
    db: AsyncSession = None,
) -> MatchmakingRequest:
    """创建组局请求

    Args:
        creator_id: 创建者用户 ID
        title: 组局标题
        scheduled_time: 预定时间
        location: 地点
        latitude: 纬度
        longitude: 经度
        min_rank: 最低段位要求
        max_rank: 最高段位要求
        industry_tag: 行业标签
        max_players: 最大人数
        deposit_amount: 押金金额
        db: 数据库 Session

    Returns:
        创建的 MatchmakingRequest 对象
    """
    request = MatchmakingRequest(
        creator_id=creator_id,
        title=title,
        scheduled_time=scheduled_time,
        location=location,
        latitude=latitude,
        longitude=longitude,
        min_rank=min_rank,
        max_rank=max_rank,
        industry_tag=industry_tag,
        max_players=max_players,
        current_players=1,
        deposit_amount=deposit_amount,
        status="open",
    )
    db.add(request)
    await db.flush()

    # 创建者自动加入为参与者
    participant = MatchmakingParticipant(
        request_id=request.id,
        user_id=creator_id,
        status="joined",
    )
    db.add(participant)
    await db.commit()
    await db.refresh(request)
    return request


async def get_matchmaking_list(
    page: int = 1,
    page_size: int = 20,
    status_filter: str | None = None,
    rank_filter: str | None = None,
    industry_filter: str | None = None,
    db: AsyncSession = None,
) -> dict:
    """分页获取组局列表

    Args:
        page: 页码（从1开始）
        page_size: 每页数量
        status_filter: 状态筛选
        rank_filter: 段位筛选
        industry_filter: 行业筛选
        db: 数据库 Session

    Returns:
        {"items": [...], "total": int, "page": int, "page_size": int}
    """
    query = select(MatchmakingRequest)
    count_query = select(func.count(MatchmakingRequest.id))

    if status_filter:
        query = query.where(MatchmakingRequest.status == status_filter)
        count_query = count_query.where(MatchmakingRequest.status == status_filter)

    if rank_filter:
        query = query.where(MatchmakingRequest.min_rank == rank_filter)
        count_query = count_query.where(MatchmakingRequest.min_rank == rank_filter)

    if industry_filter:
        query = query.where(MatchmakingRequest.industry_tag == industry_filter)
        count_query = count_query.where(MatchmakingRequest.industry_tag == industry_filter)

    # 按创建时间倒序
    query = query.order_by(MatchmakingRequest.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    items = result.scalars().all()

    count_result = await db.execute(count_query)
    total = count_result.scalar()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


async def join_matchmaking(
    request_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> MatchmakingParticipant:
    """加入组局

    检查：
    1. 组局存在且状态为 open
    2. 用户未已加入
    3. 未达到最大人数

    自动设置 status="full" 当达到 max_players。

    Args:
        request_id: 组局请求 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        创建的 MatchmakingParticipant

    Raises:
        ValueError: 各种业务规则不满足
    """
    # 获取组局请求
    result = await db.execute(
        select(MatchmakingRequest).where(MatchmakingRequest.id == request_id)
    )
    request = result.scalar_one_or_none()

    if request is None:
        raise ValueError("组局不存在")

    if request.status != "open":
        raise ValueError("组局已满员或已关闭")

    # 检查是否已加入
    existing = await db.execute(
        select(MatchmakingParticipant).where(
            MatchmakingParticipant.request_id == request_id,
            MatchmakingParticipant.user_id == user_id,
            MatchmakingParticipant.status == "joined",
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise ValueError("您已加入该组局")

    # 检查容量
    if request.current_players >= request.max_players:
        raise ValueError("组局人数已满")

    # 创建参与者
    participant = MatchmakingParticipant(
        request_id=request_id,
        user_id=user_id,
        status="joined",
    )
    db.add(participant)

    # 更新人数
    request.current_players += 1

    # 自动满员
    if request.current_players >= request.max_players:
        request.status = "full"

    await db.commit()
    await db.refresh(participant)
    return participant


async def cancel_participation(
    request_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> dict:
    """取消参加组局

    规则：
    - 距预定时间 < 2 小时：扣押金（forfeit）
    - 距预定时间 >= 2 小时：全额退还

    Args:
        request_id: 组局请求 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        {"success": True, "refund": bool, "message": str}

    Raises:
        ValueError: 业务规则不满足
    """
    # 获取组局请求
    result = await db.execute(
        select(MatchmakingRequest).where(MatchmakingRequest.id == request_id)
    )
    request = result.scalar_one_or_none()

    if request is None:
        raise ValueError("组局不存在")

    # 获取参与记录
    participant_result = await db.execute(
        select(MatchmakingParticipant).where(
            MatchmakingParticipant.request_id == request_id,
            MatchmakingParticipant.user_id == user_id,
            MatchmakingParticipant.status == "joined",
        )
    )
    participant = participant_result.scalar_one_or_none()

    if participant is None:
        raise ValueError("您未参加该组局")

    # 判断是否 < 2 小时
    now = datetime.now(timezone.utc)
    time_until_start = request.scheduled_time.replace(tzinfo=timezone.utc) - now
    forfeit_deposit = time_until_start < timedelta(hours=2)

    # 取消参与
    participant.status = "cancelled"
    participant.cancelled_at = now

    # 减少人数
    request.current_players -= 1
    if request.status == "full":
        request.status = "open"

    await db.commit()

    if forfeit_deposit:
        return {
            "success": True,
            "refund": False,
            "message": "距开始不足2小时，押金不予退还",
        }
    else:
        return {
            "success": True,
            "refund": True,
            "message": "已取消参加，押金将全额退还",
        }

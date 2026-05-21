"""赛事服务 - 赛事创建、报名、签到、成绩录入

核心功能：
- create_event: 创建赛事
- get_events: 分页获取赛事列表
- get_event_detail: 获取赛事详情
- register_event: 赛事报名（容量检查）
- cancel_registration: 取消报名（截止时间检查）
- checkin: 签到
- submit_scores: 提交成绩（调用 elo_service 更新积分）
"""

from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event, EventRegistration
from app.models.elo import MatchResult
from app.services import elo_service


async def create_event(
    organizer_id: int,
    title: str,
    event_date: datetime,
    description: str | None = None,
    location: str | None = None,
    entry_fee: float = 0.00,
    max_capacity: int = 100,
    rules: str | None = None,
    cancel_deadline: datetime | None = None,
    db: AsyncSession = None,
) -> Event:
    """创建赛事

    Args:
        organizer_id: 组织者用户 ID
        title: 赛事标题
        event_date: 赛事日期
        description: 赛事描述
        location: 赛事地点
        entry_fee: 报名费
        max_capacity: 最大参赛人数
        rules: 赛事规则
        cancel_deadline: 取消报名截止时间
        db: 数据库 Session

    Returns:
        创建的 Event 对象
    """
    event = Event(
        organizer_id=organizer_id,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        entry_fee=entry_fee,
        max_capacity=max_capacity,
        rules=rules,
        cancel_deadline=cancel_deadline,
        status="upcoming",
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def get_events(
    page: int = 1,
    page_size: int = 20,
    status_filter: str | None = None,
    db: AsyncSession = None,
) -> dict:
    """分页获取赛事列表

    Args:
        page: 页码（从1开始）
        page_size: 每页数量
        status_filter: 状态筛选
        db: 数据库 Session

    Returns:
        {"items": [...], "total": int, "page": int, "page_size": int}
    """
    query = select(Event)
    count_query = select(func.count(Event.id))

    if status_filter:
        query = query.where(Event.status == status_filter)
        count_query = count_query.where(Event.status == status_filter)

    query = query.order_by(Event.event_date.desc())
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


async def get_event_detail(
    event_id: int,
    db: AsyncSession = None,
) -> Event | None:
    """获取赛事详情

    Args:
        event_id: 赛事 ID
        db: 数据库 Session

    Returns:
        Event 对象或 None
    """
    result = await db.execute(select(Event).where(Event.id == event_id))
    return result.scalar_one_or_none()


async def register_event(
    event_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> EventRegistration:
    """赛事报名

    检查：
    1. 赛事存在且状态为 upcoming
    2. 用户未已报名
    3. 未达到最大容量

    Args:
        event_id: 赛事 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        创建的 EventRegistration

    Raises:
        ValueError: 业务规则不满足
    """
    # 获取赛事
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if event is None:
        raise ValueError("赛事不存在")

    if event.status not in ("upcoming", "ongoing"):
        raise ValueError("赛事不在报名阶段")

    # 检查容量
    if event.current_registrations >= event.max_capacity:
        raise ValueError("报名人数已满")

    # 检查是否已报名
    existing = await db.execute(
        select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id,
            EventRegistration.status == "registered",
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise ValueError("您已报名该赛事")

    # 创建报名
    registration = EventRegistration(
        event_id=event_id,
        user_id=user_id,
        status="registered",
    )
    db.add(registration)

    # 更新报名人数
    event.current_registrations += 1

    await db.commit()
    await db.refresh(registration)
    return registration


async def cancel_registration(
    event_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> bool:
    """取消报名

    检查 cancel_deadline 是否已过。

    Args:
        event_id: 赛事 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        True 表示成功

    Raises:
        ValueError: 业务规则不满足
    """
    # 获取赛事
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if event is None:
        raise ValueError("赛事不存在")

    # 检查截止时间
    now = datetime.now(timezone.utc)
    if event.cancel_deadline and now > event.cancel_deadline.replace(tzinfo=timezone.utc):
        raise ValueError("已过取消报名截止时间")

    # 获取报名记录
    reg_result = await db.execute(
        select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id,
            EventRegistration.status == "registered",
        )
    )
    registration = reg_result.scalar_one_or_none()

    if registration is None:
        raise ValueError("您未报名该赛事")

    registration.status = "cancelled"
    event.current_registrations -= 1

    await db.commit()
    return True


async def checkin(
    event_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> EventRegistration:
    """赛事签到

    Args:
        event_id: 赛事 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        更新后的 EventRegistration

    Raises:
        ValueError: 业务规则不满足
    """
    # 获取报名记录
    reg_result = await db.execute(
        select(EventRegistration).where(
            EventRegistration.event_id == event_id,
            EventRegistration.user_id == user_id,
            EventRegistration.status == "registered",
        )
    )
    registration = reg_result.scalar_one_or_none()

    if registration is None:
        raise ValueError("未找到有效报名记录")

    registration.status = "checked_in"
    registration.checked_in_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(registration)
    return registration


async def submit_scores(
    event_id: int,
    results: list[dict],
    recorded_by: int,
    db: AsyncSession = None,
) -> list[MatchResult]:
    """提交赛事成绩

    对每对 winner/loser 调用 elo_service.record_match_result 更新积分。

    Args:
        event_id: 赛事 ID
        results: [{"winner_id": int, "loser_id": int}, ...]
        recorded_by: 记录者用户 ID
        db: 数据库 Session

    Returns:
        创建的 MatchResult 列表

    Raises:
        ValueError: 赛事不存在
    """
    # 验证赛事存在
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()

    if event is None:
        raise ValueError("赛事不存在")

    match_results = []
    for item in results:
        match_result = await elo_service.record_match_result(
            winner_id=item["winner_id"],
            loser_id=item["loser_id"],
            db=db,
            event_id=event_id,
            recorded_by=recorded_by,
        )
        match_results.append(match_result)

    await db.commit()
    return match_results

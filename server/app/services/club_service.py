"""俱乐部服务 - 创建俱乐部、加入、成员管理、活动管理

核心功能：
- create_club: 创建俱乐部
- get_clubs: 分页获取俱乐部列表
- get_club_detail: 获取俱乐部详情
- join_club: 加入俱乐部（容量检查）
- get_members: 获取成员列表
- create_activity: 创建俱乐部活动
- get_activities: 获取俱乐部活动列表
"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.club import Club, ClubActivity, ClubMember


async def create_club(
    owner_id: int,
    name: str,
    description: str | None = None,
    region: str | None = None,
    membership_fee: float = 0.00,
    max_members: int = 200,
    db: AsyncSession = None,
) -> Club:
    """创建俱乐部

    创建者自动成为 owner 角色成员。

    Args:
        owner_id: 创建者用户 ID
        name: 俱乐部名称
        description: 俱乐部描述
        region: 所在地区
        membership_fee: 会员费
        max_members: 最大成员数
        db: 数据库 Session

    Returns:
        创建的 Club 对象
    """
    club = Club(
        owner_id=owner_id,
        name=name,
        description=description,
        region=region,
        membership_fee=membership_fee,
        max_members=max_members,
        current_members=1,
        status="active",
    )
    db.add(club)
    await db.flush()

    # 创建者自动成为 owner 成员
    member = ClubMember(
        club_id=club.id,
        user_id=owner_id,
        role="owner",
        status="active",
    )
    db.add(member)
    await db.commit()
    await db.refresh(club)
    return club


async def get_clubs(
    page: int = 1,
    page_size: int = 20,
    region_filter: str | None = None,
    db: AsyncSession = None,
) -> dict:
    """分页获取俱乐部列表

    Args:
        page: 页码（从1开始）
        page_size: 每页数量
        region_filter: 地区筛选
        db: 数据库 Session

    Returns:
        {"items": [...], "total": int, "page": int, "page_size": int}
    """
    query = select(Club).where(Club.status == "active")
    count_query = select(func.count(Club.id)).where(Club.status == "active")

    if region_filter:
        query = query.where(Club.region == region_filter)
        count_query = count_query.where(Club.region == region_filter)

    query = query.order_by(Club.created_at.desc())
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


async def get_club_detail(
    club_id: int,
    db: AsyncSession = None,
) -> Club | None:
    """获取俱乐部详情

    Args:
        club_id: 俱乐部 ID
        db: 数据库 Session

    Returns:
        Club 对象或 None
    """
    result = await db.execute(select(Club).where(Club.id == club_id))
    return result.scalar_one_or_none()


async def join_club(
    club_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> ClubMember:
    """加入俱乐部

    检查：
    1. 俱乐部存在且活跃
    2. 用户未已加入
    3. 未达到最大成员数

    Args:
        club_id: 俱乐部 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        创建的 ClubMember

    Raises:
        ValueError: 业务规则不满足
    """
    # 获取俱乐部
    result = await db.execute(select(Club).where(Club.id == club_id))
    club = result.scalar_one_or_none()

    if club is None:
        raise ValueError("俱乐部不存在")

    if club.status != "active":
        raise ValueError("俱乐部已停用")

    # 检查容量
    if club.current_members >= club.max_members:
        raise ValueError("俱乐部成员已满")

    # 检查是否已加入
    existing = await db.execute(
        select(ClubMember).where(
            ClubMember.club_id == club_id,
            ClubMember.user_id == user_id,
            ClubMember.status == "active",
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise ValueError("您已是该俱乐部成员")

    # 创建成员
    member = ClubMember(
        club_id=club_id,
        user_id=user_id,
        role="member",
        status="active",
    )
    db.add(member)

    # 更新成员数
    club.current_members += 1

    await db.commit()
    await db.refresh(member)
    return member


async def get_members(
    club_id: int,
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = None,
) -> dict:
    """获取俱乐部成员列表

    Args:
        club_id: 俱乐部 ID
        page: 页码
        page_size: 每页数量
        db: 数据库 Session

    Returns:
        {"items": [...], "total": int, "page": int, "page_size": int}
    """
    query = select(ClubMember).where(
        ClubMember.club_id == club_id,
        ClubMember.status == "active",
    )
    count_query = select(func.count(ClubMember.id)).where(
        ClubMember.club_id == club_id,
        ClubMember.status == "active",
    )

    query = query.order_by(ClubMember.joined_at.asc())
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


async def create_activity(
    club_id: int,
    creator_id: int,
    title: str,
    description: str | None = None,
    activity_time: str | None = None,
    location: str | None = None,
    db: AsyncSession = None,
) -> ClubActivity:
    """创建俱乐部活动

    Args:
        club_id: 俱乐部 ID
        creator_id: 创建者用户 ID
        title: 活动标题
        description: 活动描述
        activity_time: 活动时间
        location: 活动地点
        db: 数据库 Session

    Returns:
        创建的 ClubActivity

    Raises:
        ValueError: 俱乐部不存在
    """
    # 验证俱乐部存在
    result = await db.execute(select(Club).where(Club.id == club_id))
    club = result.scalar_one_or_none()

    if club is None:
        raise ValueError("俱乐部不存在")

    activity = ClubActivity(
        club_id=club_id,
        creator_id=creator_id,
        title=title,
        description=description,
        activity_time=activity_time,
        location=location,
        status="upcoming",
    )
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity


async def get_activities(
    club_id: int,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = None,
) -> dict:
    """获取俱乐部活动列表

    Args:
        club_id: 俱乐部 ID
        page: 页码
        page_size: 每页数量
        db: 数据库 Session

    Returns:
        {"items": [...], "total": int, "page": int, "page_size": int}
    """
    query = select(ClubActivity).where(ClubActivity.club_id == club_id)
    count_query = select(func.count(ClubActivity.id)).where(
        ClubActivity.club_id == club_id
    )

    query = query.order_by(ClubActivity.created_at.desc())
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

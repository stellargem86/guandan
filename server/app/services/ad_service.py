"""广告服务 - 投放配置、展示计数、点击追踪

提供以下功能：
- get_active_ads: 获取指定位置的活跃广告
- record_impression: 记录广告曝光（原子递增）
- record_click: 记录广告点击（原子递增）
- create_ad: 创建广告
- update_ad: 更新广告
"""

from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Advertisement

# 允许的广告位置
VALID_POSITIONS = ["home_banner", "feed_card", "event_banner", "news_feed"]


class AdServiceError(Exception):
    """广告服务异常"""

    def __init__(self, message: str, code: str = "AD_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


async def get_active_ads(
    db: AsyncSession,
    position: str,
) -> list[Advertisement]:
    """获取指定位置的活跃广告

    筛选条件：
    - 位置匹配
    - 状态为 active
    - 当前时间在 start_date 和 end_date 之间（如果设置了的话）

    Args:
        db: 数据库 Session
        position: 广告位置 (home_banner/feed_card/event_banner/news_feed)

    Returns:
        活跃广告列表
    """
    if position not in VALID_POSITIONS:
        raise AdServiceError(
            message=f"无效的广告位置: {position}，允许的位置: {', '.join(VALID_POSITIONS)}",
            code="INVALID_POSITION",
        )

    now = datetime.now(timezone.utc)

    query = (
        select(Advertisement)
        .where(
            Advertisement.position == position,
            Advertisement.status == "active",
        )
    )

    result = await db.execute(query)
    ads = list(result.scalars().all())

    # 在 Python 层过滤日期范围（因为 start_date 和 end_date 可以为 None）
    active_ads = []
    for ad in ads:
        # 如果设置了开始时间，当前时间必须在开始时间之后
        if ad.start_date and now < ad.start_date:
            continue
        # 如果设置了结束时间，当前时间必须在结束时间之前
        if ad.end_date and now > ad.end_date:
            continue
        active_ads.append(ad)

    return active_ads


async def record_impression(db: AsyncSession, ad_id: int) -> None:
    """记录广告曝光（原子递增 impressions 计数）

    Args:
        db: 数据库 Session
        ad_id: 广告ID

    Raises:
        AdServiceError: 广告不存在
    """
    stmt = (
        update(Advertisement)
        .where(Advertisement.id == ad_id)
        .values(impressions=Advertisement.impressions + 1)
    )
    result = await db.execute(stmt)

    if result.rowcount == 0:
        raise AdServiceError(
            message="广告不存在",
            code="AD_NOT_FOUND",
        )


async def record_click(db: AsyncSession, ad_id: int) -> None:
    """记录广告点击（原子递增 clicks 计数）

    Args:
        db: 数据库 Session
        ad_id: 广告ID

    Raises:
        AdServiceError: 广告不存在
    """
    stmt = (
        update(Advertisement)
        .where(Advertisement.id == ad_id)
        .values(clicks=Advertisement.clicks + 1)
    )
    result = await db.execute(stmt)

    if result.rowcount == 0:
        raise AdServiceError(
            message="广告不存在",
            code="AD_NOT_FOUND",
        )


async def create_ad(
    db: AsyncSession,
    title: str,
    image_url: str,
    link_url: str | None,
    position: str,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> Advertisement:
    """创建广告

    Args:
        db: 数据库 Session
        title: 广告标题
        image_url: 广告图片URL
        link_url: 点击跳转链接
        position: 投放位置
        start_date: 投放开始时间
        end_date: 投放结束时间

    Returns:
        创建的 Advertisement ORM 对象

    Raises:
        AdServiceError: 位置无效
    """
    if position not in VALID_POSITIONS:
        raise AdServiceError(
            message=f"无效的广告位置: {position}",
            code="INVALID_POSITION",
        )

    ad = Advertisement(
        title=title,
        image_url=image_url,
        link_url=link_url,
        position=position,
        start_date=start_date,
        end_date=end_date,
        status="active",
    )
    db.add(ad)
    await db.flush()
    return ad


async def update_ad(db: AsyncSession, ad_id: int, **updates) -> Advertisement:
    """更新广告

    Args:
        db: 数据库 Session
        ad_id: 广告ID
        **updates: 要更新的字段

    Returns:
        更新后的 Advertisement ORM 对象

    Raises:
        AdServiceError: 广告不存在或位置无效
    """
    # 验证位置
    if "position" in updates and updates["position"] not in VALID_POSITIONS:
        raise AdServiceError(
            message=f"无效的广告位置: {updates['position']}",
            code="INVALID_POSITION",
        )

    # 过滤掉 None 值
    valid_updates = {k: v for k, v in updates.items() if v is not None}

    if not valid_updates:
        raise AdServiceError(
            message="没有需要更新的字段",
            code="NO_UPDATES",
        )

    # 执行更新
    stmt = (
        update(Advertisement)
        .where(Advertisement.id == ad_id)
        .values(**valid_updates)
    )
    result = await db.execute(stmt)

    if result.rowcount == 0:
        raise AdServiceError(
            message="广告不存在",
            code="AD_NOT_FOUND",
        )

    # 刷新并返回更新后的对象
    await db.flush()
    query_result = await db.execute(
        select(Advertisement).where(Advertisement.id == ad_id)
    )
    ad = query_result.scalar_one_or_none()

    return ad

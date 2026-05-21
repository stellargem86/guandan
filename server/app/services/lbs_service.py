"""LBS 地理位置服务 - 商户位置同步与附近查询

提供功能：
- sync_all_merchants_to_redis: 将所有活跃商户的位置批量写入 Redis GEO
- sync_merchant_location: 单个商户位置更新
- remove_merchant_from_geo: 移除商户地理位置
- get_nearby_merchants: 查询附近商户（距离排序 + 分页）
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_manager
from app.models.merchant import Merchant


async def sync_all_merchants_to_redis(db: AsyncSession) -> int:
    """将所有活跃商户的位置数据批量同步到 Redis GEO

    查询数据库中所有 status='active' 且有经纬度数据的商户，
    使用 batch GEOADD 写入 Redis geo:merchants 键。

    Args:
        db: 数据库 Session

    Returns:
        成功同步的商户数量
    """
    stmt = select(Merchant).where(
        Merchant.status == "active",
        Merchant.latitude.isnot(None),
        Merchant.longitude.isnot(None),
    )
    result = await db.execute(stmt)
    merchants = result.scalars().all()

    if not merchants:
        return 0

    # 构建批量数据: [(merchant_id, longitude, latitude), ...]
    locations: list[tuple[str, float, float]] = []
    for m in merchants:
        locations.append((str(m.id), float(m.longitude), float(m.latitude)))

    await redis_manager.geo_add_merchants_batch(locations)
    return len(locations)


async def sync_merchant_location(
    merchant_id: int, lat: float, lng: float
) -> None:
    """更新单个商户在 Redis GEO 中的位置

    Args:
        merchant_id: 商户 ID
        lat: 纬度
        lng: 经度
    """
    await redis_manager.geo_add_merchant(str(merchant_id), lng, lat)


async def remove_merchant_from_geo(merchant_id: int) -> None:
    """从 Redis GEO 中移除商户

    Args:
        merchant_id: 商户 ID
    """
    await redis_manager.geo_remove_merchant(str(merchant_id))


async def get_nearby_merchants(
    db: AsyncSession,
    lat: float,
    lng: float,
    radius_km: float = 5.0,
    page: int = 1,
    page_size: int = 20,
) -> list[dict]:
    """查询附近商户，按距离排序并分页

    1. 调用 Redis GEOSEARCH 获取范围内的商户 ID 和距离
    2. 从数据库批量获取商户详情
    3. 按距离升序排序后分页返回

    Args:
        db: 数据库 Session
        lat: 用户纬度
        lng: 用户经度
        radius_km: 搜索半径 (km)，默认 5.0
        page: 页码 (从 1 开始)
        page_size: 每页数量，默认 20

    Returns:
        包含商户信息和距离的字典列表:
        [{"id", "name", "address", "latitude", "longitude", "distance_km",
          "rating", "cover_image", "business_hours", "phone"}, ...]
    """
    # 从 Redis 获取附近商户 ID + 距离
    # 获取足够多的结果用于分页（最多 count 个）
    max_count = page * page_size + page_size  # 多取一些确保分页准确
    geo_results = await redis_manager.geo_search_merchants(
        longitude=lng,
        latitude=lat,
        radius_km=radius_km,
        count=max_count,
        sort_asc=True,
    )

    if not geo_results:
        return []

    # 分页裁剪
    start = (page - 1) * page_size
    end = start + page_size
    paged_results = geo_results[start:end]

    if not paged_results:
        return []

    # 提取商户 IDs
    merchant_ids = [int(item["member"]) for item in paged_results]
    # 距离映射
    distance_map = {int(item["member"]): item["dist"] for item in paged_results}

    # 从数据库批量获取商户详情
    stmt = select(Merchant).where(Merchant.id.in_(merchant_ids))
    result = await db.execute(stmt)
    merchants = result.scalars().all()

    # 构建 ID -> Merchant 映射
    merchant_map = {m.id: m for m in merchants}

    # 按距离排序输出
    output = []
    for mid in merchant_ids:
        m = merchant_map.get(mid)
        if m is None:
            continue
        output.append({
            "id": m.id,
            "name": m.name,
            "address": m.address,
            "latitude": float(m.latitude) if m.latitude else None,
            "longitude": float(m.longitude) if m.longitude else None,
            "distance_km": round(distance_map.get(mid, 0.0), 2),
            "rating": float(m.rating) if m.rating else 0.0,
            "cover_image": m.cover_image,
            "business_hours": m.business_hours,
            "phone": m.phone,
        })

    return output

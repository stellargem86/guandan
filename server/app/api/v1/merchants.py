"""商户路由 - LBS 查询、商户详情、套餐"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.merchant import DiningPackage, Merchant
from app.services.lbs_service import get_nearby_merchants

router = APIRouter()


@router.get("/nearby")
async def get_nearby(
    lat: float = Query(..., description="用户纬度", ge=-90, le=90),
    lng: float = Query(..., description="用户经度", ge=-180, le=180),
    radius: float = Query(5.0, description="搜索半径(km)", gt=0, le=50),
    page: int = Query(1, description="页码", ge=1),
    page_size: int = Query(20, description="每页数量", ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """获取附近商户（LBS）

    基于用户经纬度，通过 Redis GEO 查询指定半径内的商户，
    按距离升序排列，支持分页。
    """
    merchants = await get_nearby_merchants(
        db=db,
        lat=lat,
        lng=lng,
        radius_km=radius,
        page=page,
        page_size=page_size,
    )
    return {"code": 0, "data": merchants, "total": len(merchants)}


@router.get("/{merchant_id}")
async def get_merchant(
    merchant_id: int,
    db: AsyncSession = Depends(get_db),
):
    """商户详情"""
    stmt = select(Merchant).where(Merchant.id == merchant_id)
    result = await db.execute(stmt)
    merchant = result.scalar_one_or_none()

    if not merchant:
        return {"code": 404, "message": "商户不存在"}

    return {
        "code": 0,
        "data": {
            "id": merchant.id,
            "name": merchant.name,
            "description": merchant.description,
            "address": merchant.address,
            "latitude": float(merchant.latitude) if merchant.latitude else None,
            "longitude": float(merchant.longitude) if merchant.longitude else None,
            "phone": merchant.phone,
            "rating": float(merchant.rating) if merchant.rating else 0.0,
            "cover_image": merchant.cover_image,
            "photos": merchant.photos,
            "business_hours": merchant.business_hours,
            "status": merchant.status,
        },
    }


@router.get("/{merchant_id}/packages")
async def list_merchant_packages(
    merchant_id: int,
    db: AsyncSession = Depends(get_db),
):
    """商户餐饮套餐列表"""
    stmt = select(DiningPackage).where(
        DiningPackage.merchant_id == merchant_id,
        DiningPackage.status == "active",
    )
    result = await db.execute(stmt)
    packages = result.scalars().all()

    data = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "original_price": float(p.original_price) if p.original_price else None,
            "cover_image": p.cover_image,
            "validity_days": p.validity_days,
            "inventory": p.inventory,
            "sold_count": p.sold_count,
        }
        for p in packages
    ]

    return {"code": 0, "data": data}

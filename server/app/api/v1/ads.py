"""广告管理路由 - 投放配置、展示计数、点击追踪

提供以下接口：
- GET /ads?position=: 获取指定位置的活跃广告（公开接口，供移动端调用）
- POST /ads/:id/impression: 记录广告曝光
- POST /ads/:id/click: 记录广告点击
- POST /admin/ads: 创建广告（仅管理员）
- PUT /admin/ads/:id: 更新广告（仅管理员）

广告位置：home_banner / feed_card / event_banner / news_feed
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.content import (
    AdvertisementCreate,
    AdvertisementResponse,
    AdvertisementUpdate,
)
from app.services.ad_service import (
    AdServiceError,
    create_ad,
    get_active_ads,
    record_click,
    record_impression,
    update_ad,
)

router = APIRouter()


@router.get("", response_model=list[AdvertisementResponse])
async def list_active_ads(
    position: str = Query(..., description="广告位置"),
    db: AsyncSession = Depends(get_db),
):
    """获取指定位置的活跃广告（公开接口）

    供移动端使用，返回当前有效的广告列表。
    位置：home_banner / feed_card / event_banner / news_feed
    """
    try:
        ads = await get_active_ads(db=db, position=position)
    except AdServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    return [AdvertisementResponse.model_validate(ad) for ad in ads]


@router.post("/{ad_id}/impression", status_code=status.HTTP_204_NO_CONTENT)
async def record_ad_impression(
    ad_id: int,
    db: AsyncSession = Depends(get_db),
):
    """记录广告曝光

    移动端每次展示广告时调用，原子递增曝光计数。
    """
    try:
        await record_impression(db=db, ad_id=ad_id)
    except AdServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post("/{ad_id}/click", status_code=status.HTTP_204_NO_CONTENT)
async def record_ad_click(
    ad_id: int,
    db: AsyncSession = Depends(get_db),
):
    """记录广告点击

    移动端用户点击广告时调用，原子递增点击计数。
    """
    try:
        await record_click(db=db, ad_id=ad_id)
    except AdServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post("/manage", response_model=AdvertisementResponse, status_code=status.HTTP_201_CREATED)
async def create_ad_endpoint(
    body: AdvertisementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """创建广告（仅管理员）"""
    try:
        ad = await create_ad(
            db=db,
            title=body.title,
            image_url=body.image_url,
            link_url=body.link_url,
            position=body.position,
            start_date=body.start_date,
            end_date=body.end_date,
        )
    except AdServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    return AdvertisementResponse.model_validate(ad)


@router.put("/manage/{ad_id}", response_model=AdvertisementResponse)
async def update_ad_endpoint(
    ad_id: int,
    body: AdvertisementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """更新广告（仅管理员）"""
    try:
        ad = await update_ad(
            db=db,
            ad_id=ad_id,
            **body.model_dump(exclude_unset=True),
        )
    except AdServiceError as e:
        if e.code == "AD_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    return AdvertisementResponse.model_validate(ad)

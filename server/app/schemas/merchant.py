"""商户 & 餐饮套餐 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Merchant Schemas
# ============================================================


class MerchantBase(BaseModel):
    """商户基础字段"""

    name: str = Field(..., max_length=128, description="商户名称")
    description: str | None = Field(None, description="商户描述")
    address: str | None = Field(None, max_length=256, description="地址")
    latitude: Decimal | None = Field(None, description="纬度")
    longitude: Decimal | None = Field(None, description="经度")
    geohash: str | None = Field(None, max_length=12, description="GeoHash")
    phone: str | None = Field(None, max_length=20, description="联系电话")
    cover_image: str | None = Field(None, max_length=512, description="封面图片")
    photos: list | None = Field(default_factory=list, description="商户图片数组")
    business_hours: str | None = Field(None, max_length=128, description="营业时间")


class MerchantCreate(MerchantBase):
    """创建商户"""

    user_id: int = Field(..., description="关联管理员用户ID")
    bank_account: str | None = Field(None, max_length=64, description="结算银行账户")
    commission_rate: Decimal = Field(
        default=Decimal("0.100"), description="平台佣金比例"
    )


class MerchantUpdate(BaseModel):
    """更新商户（所有字段可选）"""

    name: str | None = Field(None, max_length=128)
    description: str | None = None
    address: str | None = Field(None, max_length=256)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    geohash: str | None = Field(None, max_length=12)
    phone: str | None = Field(None, max_length=20)
    cover_image: str | None = Field(None, max_length=512)
    photos: list | None = None
    business_hours: str | None = Field(None, max_length=128)
    bank_account: str | None = Field(None, max_length=64)
    commission_rate: Decimal | None = None
    status: str | None = Field(None, max_length=20)


class MerchantInDB(MerchantBase):
    """数据库中的商户"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    rating: Decimal = Decimal("0.00")
    bank_account: str | None = None
    commission_rate: Decimal = Decimal("0.100")
    status: str = "pending"
    created_at: datetime
    updated_at: datetime


class MerchantResponse(MerchantInDB):
    """商户 API 响应"""

    pass


# ============================================================
# DiningPackage Schemas
# ============================================================


class DiningPackageBase(BaseModel):
    """餐饮套餐基础字段"""

    name: str = Field(..., max_length=128, description="套餐名称")
    description: str | None = Field(None, description="套餐描述")
    price: Decimal = Field(..., description="售价（元）")
    original_price: Decimal | None = Field(None, description="原价")
    cover_image: str | None = Field(None, max_length=512, description="封面图片")
    validity_days: int = Field(default=30, description="有效天数")
    inventory: int = Field(default=999, description="库存")


class DiningPackageCreate(DiningPackageBase):
    """创建餐饮套餐"""

    merchant_id: int = Field(..., description="所属商户ID")


class DiningPackageUpdate(BaseModel):
    """更新餐饮套餐（所有字段可选）"""

    name: str | None = Field(None, max_length=128)
    description: str | None = None
    price: Decimal | None = None
    original_price: Decimal | None = None
    cover_image: str | None = Field(None, max_length=512)
    validity_days: int | None = None
    inventory: int | None = None
    status: str | None = Field(None, max_length=20)


class DiningPackageInDB(DiningPackageBase):
    """数据库中的餐饮套餐"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    merchant_id: int
    sold_count: int = 0
    status: str = "active"
    created_at: datetime
    updated_at: datetime


class DiningPackageResponse(DiningPackageInDB):
    """餐饮套餐 API 响应"""

    pass

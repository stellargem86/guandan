"""商户模型 (Merchants) + 餐饮套餐模型 (Dining Packages)

对应 DDL: merchants 表, dining_packages 表
商户包含地理位置信息、佣金配置等；餐饮套餐属于商户下的子资源。
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Merchant(Base):
    """商户表 ORM 模型"""

    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="关联管理员用户"
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False, comment="商户名称"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="商户描述"
    )
    address: Mapped[str | None] = mapped_column(
        String(256), nullable=True, comment="地址"
    )
    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True, comment="纬度"
    )
    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True, comment="经度"
    )
    geohash: Mapped[str | None] = mapped_column(
        String(12), nullable=True, comment="GeoHash 索引"
    )
    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="联系电话"
    )
    rating: Mapped[Decimal] = mapped_column(
        Numeric(3, 2), server_default="0.00", comment="评分"
    )
    cover_image: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="封面图片"
    )
    photos: Mapped[dict | None] = mapped_column(
        JSONB, server_default="'[]'", comment="商户图片数组"
    )
    business_hours: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="营业时间"
    )
    bank_account: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="结算银行账户"
    )
    commission_rate: Mapped[Decimal] = mapped_column(
        Numeric(4, 3), server_default="0.100", comment="平台佣金比例，默认10%"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="pending",
        comment="状态: pending / active / suspended"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    packages: Mapped[list["DiningPackage"]] = relationship(
        "DiningPackage", back_populates="merchant", lazy="selectin"
    )

    __table_args__ = (
        Index("idx_merchants_geohash", "geohash"),
        Index("idx_merchants_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<Merchant(id={self.id}, name={self.name})>"


class DiningPackage(Base):
    """餐饮套餐表 ORM 模型"""

    __tablename__ = "dining_packages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    merchant_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="所属商户"
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False, comment="套餐名称"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="套餐描述"
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, comment="售价（元）"
    )
    original_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True, comment="原价"
    )
    cover_image: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="封面图片"
    )
    validity_days: Mapped[int] = mapped_column(
        Integer, server_default="30", comment="有效天数"
    )
    inventory: Mapped[int] = mapped_column(
        Integer, server_default="999", comment="库存"
    )
    sold_count: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="已售数量"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="active",
        comment="状态: active / offline / soldout"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    merchant: Mapped["Merchant"] = relationship(
        "Merchant", back_populates="packages"
    )

    __table_args__ = (
        Index("idx_dining_packages_merchant", "merchant_id", "status"),
    )

    def __repr__(self) -> str:
        return f"<DiningPackage(id={self.id}, name={self.name}, price={self.price})>"

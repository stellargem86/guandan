"""订单模型 (Orders) + 分账记录模型 (Revenue Splits)

对应 DDL: orders 表, revenue_splits 表
订单统一管理所有支付场景；分账记录跟踪每笔订单的分账明细。
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Order(Base):
    """订单表 ORM 模型"""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_no: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, comment="订单号（业务唯一）"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="下单用户"
    )
    order_type: Mapped[str] = mapped_column(
        String(30), nullable=False,
        comment="订单类型: dining_package / event_reg / club_membership / matchmaking_deposit / withdrawal"
    )
    target_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="关联业务 ID（套餐ID/赛事ID等）"
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, comment="支付金额"
    )
    wechat_transaction_id: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="微信支付交易号"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="pending",
        comment="状态: pending / paid / refunded / cancelled / failed"
    )
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="支付时间"
    )
    refunded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="退款时间"
    )
    verification_code: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="核销码（餐饮套餐用）"
    )
    verification_qr_url: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="核销二维码 URL"
    )
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="核销时间"
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="核销码过期时间"
    )
    idempotency_key: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True, comment="幂等键，防止重复支付"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    revenue_splits: Mapped[list["RevenueSplit"]] = relationship(
        "RevenueSplit", back_populates="order", lazy="selectin"
    )

    __table_args__ = (
        Index("idx_orders_user", "user_id", "created_at"),
        Index("idx_orders_order_no", "order_no"),
        Index("idx_orders_status", "status"),
        Index(
            "idx_orders_verification", "verification_code",
            postgresql_where="verification_code IS NOT NULL"
        ),
    )

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, order_no={self.order_no}, status={self.status})>"


class RevenueSplit(Base):
    """分账记录表 ORM 模型"""

    __tablename__ = "revenue_splits"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="关联订单"
    )
    receiver_type: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="收款方类型: platform / merchant / organizer"
    )
    receiver_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="收款方 ID"
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, comment="分账金额"
    )
    ratio: Mapped[Decimal] = mapped_column(
        Numeric(4, 3), nullable=False, comment="分账比例"
    )
    wechat_split_id: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="微信分账单号"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="pending",
        comment="状态: pending / completed / failed"
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="完成时间"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="revenue_splits")

    __table_args__ = (
        Index("idx_revenue_splits_order", "order_id"),
        Index("idx_revenue_splits_receiver", "receiver_type", "receiver_id"),
    )

    def __repr__(self) -> str:
        return f"<RevenueSplit(id={self.id}, order_id={self.order_id}, amount={self.amount})>"

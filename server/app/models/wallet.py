"""钱包模型 (Wallets) + 钱包交易记录模型 (Wallet Transactions)

对应 DDL: wallets 表, wallet_transactions 表
钱包管理用户余额与冻结金额；交易记录跟踪每笔收支流水。
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Wallet(Base):
    """数字钱包表 ORM 模型"""

    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="所属用户"
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), server_default="0.00", comment="可用余额"
    )
    frozen_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), server_default="0.00", comment="冻结金额"
    )
    total_income: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), server_default="0.00", comment="累计收入"
    )
    total_expense: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), server_default="0.00", comment="累计支出"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    transactions: Mapped[list["WalletTransaction"]] = relationship(
        "WalletTransaction", back_populates="wallet", lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_wallets_user_id"),
    )

    def __repr__(self) -> str:
        return f"<Wallet(id={self.id}, user_id={self.user_id}, balance={self.balance})>"


class WalletTransaction(Base):
    """钱包交易记录表 ORM 模型"""

    __tablename__ = "wallet_transactions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    wallet_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="所属钱包"
    )
    transaction_type: Mapped[str] = mapped_column(
        String(30), nullable=False, comment="交易类型"
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, comment="交易金额"
    )
    balance_after: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, comment="交易后余额"
    )
    description: Mapped[str | None] = mapped_column(
        String(256), nullable=True, comment="交易描述"
    )
    reference_id: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="关联业务单号"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="transactions")

    def __repr__(self) -> str:
        return f"<WalletTransaction(id={self.id}, type={self.transaction_type}, amount={self.amount})>"

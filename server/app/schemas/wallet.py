"""钱包 & 交易记录 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Wallet Schemas
# ============================================================


class WalletBase(BaseModel):
    """钱包基础字段"""

    user_id: int = Field(..., description="所属用户ID")


class WalletCreate(WalletBase):
    """创建钱包"""

    pass


class WalletUpdate(BaseModel):
    """更新钱包（所有字段可选）"""

    balance: Decimal | None = None
    frozen_amount: Decimal | None = None
    total_income: Decimal | None = None
    total_expense: Decimal | None = None


class WalletInDB(WalletBase):
    """数据库中的钱包"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    balance: Decimal = Decimal("0.00")
    frozen_amount: Decimal = Decimal("0.00")
    total_income: Decimal = Decimal("0.00")
    total_expense: Decimal = Decimal("0.00")
    created_at: datetime
    updated_at: datetime


class WalletResponse(WalletInDB):
    """钱包 API 响应"""

    pass


# ============================================================
# WalletTransaction Schemas
# ============================================================


class WalletTransactionBase(BaseModel):
    """钱包交易记录基础字段"""

    transaction_type: str = Field(..., max_length=30, description="交易类型")
    amount: Decimal = Field(..., description="交易金额")
    balance_after: Decimal = Field(..., description="交易后余额")
    description: str | None = Field(None, max_length=256, description="交易描述")
    reference_id: str | None = Field(None, max_length=64, description="关联业务单号")


class WalletTransactionCreate(WalletTransactionBase):
    """创建钱包交易记录"""

    wallet_id: int = Field(..., description="所属钱包ID")


class WalletTransactionUpdate(BaseModel):
    """更新钱包交易记录（所有字段可选）"""

    description: str | None = Field(None, max_length=256)


class WalletTransactionInDB(WalletTransactionBase):
    """数据库中的钱包交易记录"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    wallet_id: int
    created_at: datetime


class WalletTransactionResponse(WalletTransactionInDB):
    """钱包交易记录 API 响应"""

    pass

"""订单 & 分账记录 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Order Schemas
# ============================================================


class OrderBase(BaseModel):
    """订单基础字段"""

    order_type: str = Field(..., max_length=30, description="订单类型")
    amount: Decimal = Field(..., description="支付金额")
    target_id: int | None = Field(None, description="关联业务ID")


class OrderCreate(OrderBase):
    """创建订单"""

    user_id: int = Field(..., description="下单用户ID")
    idempotency_key: str | None = Field(None, max_length=64, description="幂等键")


class OrderUpdate(BaseModel):
    """更新订单（所有字段可选）"""

    status: str | None = Field(None, max_length=20)
    wechat_transaction_id: str | None = Field(None, max_length=64)
    paid_at: datetime | None = None
    refunded_at: datetime | None = None
    verification_code: str | None = Field(None, max_length=64)
    verification_qr_url: str | None = Field(None, max_length=512)
    verified_at: datetime | None = None
    expires_at: datetime | None = None


class OrderInDB(OrderBase):
    """数据库中的订单"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    user_id: int
    wechat_transaction_id: str | None = None
    status: str = "pending"
    paid_at: datetime | None = None
    refunded_at: datetime | None = None
    verification_code: str | None = None
    verification_qr_url: str | None = None
    verified_at: datetime | None = None
    expires_at: datetime | None = None
    idempotency_key: str | None = None
    created_at: datetime
    updated_at: datetime


class OrderResponse(OrderInDB):
    """订单 API 响应"""

    pass


# ============================================================
# RevenueSplit Schemas
# ============================================================


class RevenueSplitBase(BaseModel):
    """分账记录基础字段"""

    receiver_type: str = Field(..., max_length=20, description="收款方类型")
    receiver_id: int = Field(..., description="收款方ID")
    amount: Decimal = Field(..., description="分账金额")
    ratio: Decimal = Field(..., description="分账比例")


class RevenueSplitCreate(RevenueSplitBase):
    """创建分账记录"""

    order_id: int = Field(..., description="关联订单ID")


class RevenueSplitUpdate(BaseModel):
    """更新分账记录（所有字段可选）"""

    wechat_split_id: str | None = Field(None, max_length=64)
    status: str | None = Field(None, max_length=20)
    completed_at: datetime | None = None


class RevenueSplitInDB(RevenueSplitBase):
    """数据库中的分账记录"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    wechat_split_id: str | None = None
    status: str = "pending"
    completed_at: datetime | None = None
    created_at: datetime


class RevenueSplitResponse(RevenueSplitInDB):
    """分账记录 API 响应"""

    pass

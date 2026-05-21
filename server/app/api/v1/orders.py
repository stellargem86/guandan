"""订单路由 - 创建、查询、支付回调、核销、退款

Endpoints:
- POST /orders: 创建订单
- GET /orders/{order_id}: 订单详情
- POST /payments/callback: 微信支付回调（无认证）
- POST /orders/{order_id}/verify: 核销订单
- POST /orders/{order_id}/refund: 申请退款
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_merchant
from app.core.database import get_db
from app.core.wechat_pay import WeChatPayClient, get_wechat_pay_client
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderResponse
from app.services.payment_service import (
    PaymentServiceError,
    create_order,
    handle_payment_callback,
    process_refund,
    verify_order,
)

router = APIRouter()


# ─── Request/Response Models ───────────────────────────────────────


class CreateOrderRequest(BaseModel):
    """创建订单请求"""

    order_type: str = Field(..., description="订单类型: dining_package/event_reg/club_membership/matchmaking_deposit")
    target_id: int | None = Field(None, description="关联业务ID（套餐ID/赛事ID等）")
    amount: Decimal = Field(..., gt=0, description="支付金额（元）")
    openid: str = Field(..., description="用户微信openid")
    description: str = Field(default="深掼会平台订单", description="商品描述")


class CreateOrderResponse(BaseModel):
    """创建订单响应"""

    order_id: int
    order_no: str
    status: str
    payment_params: dict | None = None
    is_duplicate: bool = False


class VerifyOrderRequest(BaseModel):
    """核销请求"""

    verification_code: str = Field(..., min_length=1, description="核销码")
    merchant_id: int = Field(..., description="商户ID")


class RefundRequest(BaseModel):
    """退款请求"""

    reason: str = Field(default="", description="退款原因")


# ─── Endpoints ─────────────────────────────────────────────────────


@router.post("", response_model=CreateOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(
    body: CreateOrderRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    pay_client: WeChatPayClient = Depends(get_wechat_pay_client),
):
    """创建订单并发起微信支付"""
    try:
        result = await create_order(
            db=db,
            pay_client=pay_client,
            user_id=current_user.id,
            order_type=body.order_type,
            target_id=body.target_id,
            amount=body.amount,
            openid=body.openid,
            description=body.description,
        )
    except PaymentServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": e.code, "message": e.message},
        )

    order = result["order"]
    return CreateOrderResponse(
        order_id=order.id,
        order_no=order.order_no,
        status=order.status,
        payment_params=result.get("payment_params"),
        is_duplicate=result.get("is_duplicate", False),
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_endpoint(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取订单详情"""
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在",
        )

    return order


@router.post("/payments/callback")
async def payment_callback_endpoint(
    request: Request,
    db: AsyncSession = Depends(get_db),
    pay_client: WeChatPayClient = Depends(get_wechat_pay_client),
):
    """微信支付回调（无需认证，由微信服务器直接调用）

    接收微信支付结果通知，验证签名后更新订单状态。
    """
    # 读取原始 XML body
    xml_data = (await request.body()).decode("utf-8")

    response_xml = await handle_payment_callback(
        db=db,
        pay_client=pay_client,
        xml_data=xml_data,
    )

    from fastapi.responses import Response
    return Response(content=response_xml, media_type="application/xml")


@router.post("/{order_id}/verify", response_model=OrderResponse)
async def verify_order_endpoint(
    order_id: int,
    body: VerifyOrderRequest,
    current_user: User = Depends(require_merchant),
    db: AsyncSession = Depends(get_db),
):
    """核销订单（商户操作）"""
    try:
        order = await verify_order(
            db=db,
            verification_code=body.verification_code,
            merchant_id=body.merchant_id,
        )
    except PaymentServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": e.code, "message": e.message},
        )

    return order


@router.post("/{order_id}/refund", response_model=OrderResponse)
async def refund_order_endpoint(
    order_id: int,
    body: RefundRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    pay_client: WeChatPayClient = Depends(get_wechat_pay_client),
):
    """申请退款"""
    # 验证订单归属
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在",
        )

    try:
        refunded_order = await process_refund(
            db=db,
            pay_client=pay_client,
            order_id=order_id,
            reason=body.reason,
        )
    except PaymentServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": e.code, "message": e.message},
        )

    return refunded_order

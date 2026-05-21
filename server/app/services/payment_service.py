"""支付服务 - 订单创建、支付回调、核销码、退款

包含：
- create_order: 创建订单（幂等键校验、订单号生成、调用微信支付）
- handle_payment_callback: 支付回调处理（签名验证、状态更新、触发分账）
- generate_verification: 核销码生成（QR 码、过期检测）
- verify_order: 核销验证（有效性检查、标记已核销）
- process_refund: 退款服务（原路退回、状态追踪）
"""

import hashlib
import logging
import random
import string
import time
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.wechat_pay import WeChatPayClient, WeChatPayError
from app.models.merchant import DiningPackage, Merchant
from app.models.order import Order, RevenueSplit

logger = logging.getLogger(__name__)


class PaymentServiceError(Exception):
    """支付服务异常"""

    def __init__(self, message: str, code: str = "PAYMENT_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


def generate_order_no() -> str:
    """生成唯一订单号

    格式: SGH + 时间戳(13位) + 随机6位数字
    例: SGH1700000000000123456
    """
    timestamp = str(int(time.time() * 1000))
    random_part = "".join(random.choices(string.digits, k=6))
    return f"SGH{timestamp}{random_part}"


def generate_idempotency_key(user_id: int, target_id: int | None, order_type: str) -> str:
    """生成幂等键

    基于 user_id + target_id + order_type 的 SHA256 哈希
    """
    raw = f"{user_id}:{target_id or 0}:{order_type}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def generate_verification_code() -> str:
    """生成唯一12位字母数字核销码"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=12))


async def create_order(
    db: AsyncSession,
    pay_client: WeChatPayClient,
    user_id: int,
    order_type: str,
    target_id: int | None,
    amount: Decimal,
    openid: str,
    description: str = "深掼会平台订单",
) -> dict[str, Any]:
    """创建订单（幂等键校验 + 微信支付统一下单）

    Args:
        db: 数据库 Session
        pay_client: 微信支付客户端
        user_id: 下单用户 ID
        order_type: 订单类型 (dining_package/event_reg/club_membership/matchmaking_deposit)
        target_id: 关联业务 ID
        amount: 支付金额（元）
        openid: 用户微信 openid
        description: 商品描述

    Returns:
        包含订单信息和支付参数的字典

    Raises:
        PaymentServiceError: 幂等检查失败或支付创建失败
    """
    # 1. 生成幂等键并检查重复
    idempotency_key = generate_idempotency_key(user_id, target_id, order_type)

    existing = await db.execute(
        select(Order).where(Order.idempotency_key == idempotency_key)
    )
    existing_order = existing.scalar_one_or_none()

    if existing_order:
        if existing_order.status == "pending":
            # 返回已有的 pending 订单（重复请求）
            logger.info("幂等检查命中，返回已有订单: %s", existing_order.order_no)
            return {
                "order": existing_order,
                "payment_params": None,
                "is_duplicate": True,
            }
        elif existing_order.status == "paid":
            raise PaymentServiceError(
                message="该订单已支付，请勿重复下单",
                code="DUPLICATE_PAID_ORDER",
            )

    # 2. 生成订单号
    order_no = generate_order_no()

    # 3. 创建订单记录
    order = Order(
        order_no=order_no,
        user_id=user_id,
        order_type=order_type,
        target_id=target_id,
        amount=amount,
        status="pending",
        idempotency_key=idempotency_key,
    )
    db.add(order)
    await db.flush()

    # 4. 调用微信支付统一下单
    amount_cents = int(amount * 100)
    try:
        pay_result = await pay_client.create_jsapi_order(
            order_no=order_no,
            amount_cents=amount_cents,
            description=description,
            openid=openid,
        )
    except WeChatPayError as e:
        # 支付创建失败，标记订单为 failed
        order.status = "failed"
        await db.flush()
        logger.error("微信支付下单失败: order_no=%s, error=%s", order_no, e.message)
        raise PaymentServiceError(
            message=f"支付创建失败: {e.message}",
            code="WECHAT_PAY_FAILED",
        )

    logger.info("订单创建成功: order_no=%s, user_id=%d, amount=%.2f", order_no, user_id, amount)

    return {
        "order": order,
        "payment_params": pay_result.get("payment_params"),
        "prepay_id": pay_result.get("prepay_id"),
        "is_duplicate": False,
    }


async def handle_payment_callback(
    db: AsyncSession,
    pay_client: WeChatPayClient,
    xml_data: str,
) -> str:
    """处理微信支付回调

    Args:
        db: 数据库 Session
        pay_client: 微信支付客户端
        xml_data: 微信回调 XML 数据

    Returns:
        成功/失败 XML 响应字符串
    """
    SUCCESS_XML = "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
    FAIL_XML = "<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[{msg}]]></return_msg></xml>"

    # 1. 解析 XML
    callback_data = WeChatPayClient._xml_to_dict(xml_data)
    if not callback_data:
        logger.error("支付回调 XML 解析失败")
        return FAIL_XML.format(msg="XML解析失败")

    # 2. 验证签名
    signature = callback_data.pop("sign", "")
    if not pay_client.verify_callback_signature(callback_data, signature):
        logger.error("支付回调签名验证失败")
        return FAIL_XML.format(msg="签名验证失败")

    # 3. 检查支付结果
    if callback_data.get("result_code") != "SUCCESS":
        logger.warning("支付回调结果非SUCCESS: %s", callback_data.get("err_code"))
        return SUCCESS_XML  # 仍返回成功，避免微信重发

    # 4. 查找订单
    order_no = callback_data.get("out_trade_no", "")
    result = await db.execute(
        select(Order).where(Order.order_no == order_no)
    )
    order = result.scalar_one_or_none()

    if not order:
        logger.error("支付回调找不到订单: order_no=%s", order_no)
        return FAIL_XML.format(msg="订单不存在")

    # 5. 防止重复处理
    if order.status == "paid":
        logger.info("订单已支付，跳过重复回调: order_no=%s", order_no)
        return SUCCESS_XML

    # 6. 更新订单状态
    order.status = "paid"
    order.paid_at = datetime.now(timezone.utc)
    order.wechat_transaction_id = callback_data.get("transaction_id", "")
    await db.flush()

    logger.info(
        "支付回调处理成功: order_no=%s, transaction_id=%s",
        order_no,
        order.wechat_transaction_id,
    )

    # 7. 餐饮套餐订单生成核销码
    if order.order_type == "dining_package":
        try:
            await generate_verification(db, order.id)
        except Exception as e:
            logger.error("生成核销码失败: order_id=%d, error=%s", order.id, str(e))

    # 8. 触发分账（异步处理，不影响回调响应）
    try:
        from app.services.revenue_split_service import execute_revenue_split
        await execute_revenue_split(db, pay_client, order.id)
    except Exception as e:
        logger.error("触发分账失败: order_id=%d, error=%s", order.id, str(e))

    return SUCCESS_XML


async def generate_verification(
    db: AsyncSession,
    order_id: int,
    validity_days: int = 30,
) -> dict[str, Any]:
    """生成核销码和 QR URL

    Args:
        db: 数据库 Session
        order_id: 订单 ID
        validity_days: 有效天数，默认30天

    Returns:
        {"verification_code": ..., "qr_url": ..., "expires_at": ...}

    Raises:
        PaymentServiceError: 订单不存在或状态不对
    """
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise PaymentServiceError("订单不存在", code="ORDER_NOT_FOUND")

    # 生成唯一核销码
    code = generate_verification_code()
    expires_at = datetime.now(timezone.utc) + timedelta(days=validity_days)
    # QR URL 使用核销码构建（实际生产中可对接 QR 码生成服务）
    qr_url = f"https://sgh.app/verify/{code}"

    order.verification_code = code
    order.verification_qr_url = qr_url
    order.expires_at = expires_at
    await db.flush()

    logger.info("核销码生成成功: order_id=%d, code=%s", order_id, code)

    return {
        "verification_code": code,
        "qr_url": qr_url,
        "expires_at": expires_at,
    }


async def verify_order(
    db: AsyncSession,
    verification_code: str,
    merchant_id: int,
) -> Order:
    """核销订单

    Args:
        db: 数据库 Session
        verification_code: 核销码
        merchant_id: 商户 ID（用于校验订单归属）

    Returns:
        核销后的订单对象

    Raises:
        PaymentServiceError: 核销码无效、过期或已核销
    """
    # 1. 查找订单
    result = await db.execute(
        select(Order).where(Order.verification_code == verification_code)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise PaymentServiceError("核销码无效", code="INVALID_CODE")

    # 2. 检查是否已核销
    if order.verified_at is not None:
        raise PaymentServiceError("该订单已核销", code="ALREADY_VERIFIED")

    # 3. 检查是否过期
    if order.expires_at and datetime.now(timezone.utc) > order.expires_at:
        raise PaymentServiceError("核销码已过期", code="CODE_EXPIRED")

    # 4. 检查订单状态
    if order.status != "paid":
        raise PaymentServiceError("订单状态不可核销", code="INVALID_ORDER_STATUS")

    # 5. 验证订单归属商户
    if order.order_type == "dining_package" and order.target_id:
        pkg_result = await db.execute(
            select(DiningPackage).where(DiningPackage.id == order.target_id)
        )
        package = pkg_result.scalar_one_or_none()
        if package and package.merchant_id != merchant_id:
            raise PaymentServiceError("该订单不属于当前商户", code="MERCHANT_MISMATCH")

    # 6. 标记已核销
    order.verified_at = datetime.now(timezone.utc)
    await db.flush()

    logger.info("订单核销成功: order_no=%s, merchant_id=%d", order.order_no, merchant_id)
    return order


async def process_refund(
    db: AsyncSession,
    pay_client: WeChatPayClient,
    order_id: int,
    reason: str = "",
) -> Order:
    """退款处理

    Args:
        db: 数据库 Session
        pay_client: 微信支付客户端
        order_id: 订单 ID
        reason: 退款原因

    Returns:
        退款后的订单对象

    Raises:
        PaymentServiceError: 订单状态不允许退款或微信退款失败
    """
    # 1. 查找订单
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise PaymentServiceError("订单不存在", code="ORDER_NOT_FOUND")

    # 2. 校验订单状态
    if order.status != "paid":
        raise PaymentServiceError(
            f"订单状态为 {order.status}，不允许退款",
            code="INVALID_REFUND_STATUS",
        )

    if order.refunded_at is not None:
        raise PaymentServiceError("订单已退款", code="ALREADY_REFUNDED")

    # 3. 生成退款单号
    refund_no = f"REF{generate_order_no()[3:]}"

    # 4. 调用微信退款
    amount_cents = int(order.amount * 100)
    try:
        await pay_client.create_refund(
            order_no=order.order_no,
            refund_no=refund_no,
            total_amount=amount_cents,
            refund_amount=amount_cents,
            reason=reason,
        )
    except WeChatPayError as e:
        logger.error("微信退款失败: order_no=%s, error=%s", order.order_no, e.message)
        raise PaymentServiceError(
            message=f"退款失败: {e.message}",
            code="WECHAT_REFUND_FAILED",
        )

    # 5. 更新订单状态
    order.status = "refunded"
    order.refunded_at = datetime.now(timezone.utc)

    # 6. 撤销分账记录
    splits_result = await db.execute(
        select(RevenueSplit).where(RevenueSplit.order_id == order.id)
    )
    splits = splits_result.scalars().all()
    for split in splits:
        split.status = "failed"

    await db.flush()

    logger.info("退款处理成功: order_no=%s, refund_no=%s", order.order_no, refund_no)
    return order

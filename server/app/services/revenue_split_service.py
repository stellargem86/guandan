"""分账服务 - 按配置比例计算分账、调用微信分账 API

包含：
- execute_revenue_split: 执行分账（计算金额、创建记录、调用微信分账）
"""

import logging
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.wechat_pay import WeChatPayClient, WeChatPayError
from app.models.merchant import DiningPackage, Merchant
from app.models.order import Order, RevenueSplit

logger = logging.getLogger(__name__)

# 平台默认佣金比例（如果无法从商户配置获取时的兜底值）
DEFAULT_COMMISSION_RATE = Decimal("0.100")


async def execute_revenue_split(
    db: AsyncSession,
    pay_client: WeChatPayClient,
    order_id: int,
) -> list[RevenueSplit]:
    """执行分账

    根据订单类型和商户佣金配置，计算平台和商户的分账金额，
    创建分账记录并调用微信分账 API。

    Args:
        db: 数据库 Session
        pay_client: 微信支付客户端
        order_id: 订单 ID

    Returns:
        分账记录列表

    Raises:
        Exception: 分账失败时抛出
    """
    # 1. 查找订单
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        logger.error("分账失败：订单不存在 order_id=%d", order_id)
        return []

    if order.status != "paid":
        logger.warning("分账跳过：订单状态非paid order_id=%d, status=%s", order_id, order.status)
        return []

    if not order.wechat_transaction_id:
        logger.warning("分账跳过：缺少微信交易号 order_id=%d", order_id)
        return []

    # 2. 检查是否已有分账记录（防止重复分账）
    existing_result = await db.execute(
        select(RevenueSplit).where(RevenueSplit.order_id == order_id)
    )
    existing_splits = existing_result.scalars().all()
    if existing_splits:
        logger.info("分账跳过：已有分账记录 order_id=%d", order_id)
        return list(existing_splits)

    # 3. 确定佣金比例
    commission_rate = DEFAULT_COMMISSION_RATE
    merchant_id: int | None = None

    if order.order_type == "dining_package" and order.target_id:
        # 餐饮套餐：从套餐查找所属商户的佣金比例
        pkg_result = await db.execute(
            select(DiningPackage).where(DiningPackage.id == order.target_id)
        )
        package = pkg_result.scalar_one_or_none()
        if package:
            merchant_result = await db.execute(
                select(Merchant).where(Merchant.id == package.merchant_id)
            )
            merchant = merchant_result.scalar_one_or_none()
            if merchant:
                commission_rate = merchant.commission_rate
                merchant_id = merchant.id

    elif order.order_type == "event_reg":
        # 赛事报名：使用默认平台佣金（可扩展为从赛事配置读取）
        commission_rate = DEFAULT_COMMISSION_RATE

    # 4. 计算分账金额
    platform_amount = (order.amount * commission_rate).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    merchant_amount = order.amount - platform_amount

    # 5. 创建分账记录
    splits: list[RevenueSplit] = []

    # 平台分账记录
    platform_split = RevenueSplit(
        order_id=order.id,
        receiver_type="platform",
        receiver_id=0,  # 平台自身
        amount=platform_amount,
        ratio=commission_rate,
        status="pending",
    )
    db.add(platform_split)
    splits.append(platform_split)

    # 商户/组织者分账记录
    if merchant_id:
        merchant_split = RevenueSplit(
            order_id=order.id,
            receiver_type="merchant",
            receiver_id=merchant_id,
            amount=merchant_amount,
            ratio=Decimal("1.000") - commission_rate,
            status="pending",
        )
        db.add(merchant_split)
        splits.append(merchant_split)

    await db.flush()

    # 6. 调用微信分账 API
    if merchant_id and order.wechat_transaction_id:
        try:
            # 构建分账接收方列表（只分商户部分，平台部分由微信自动留存）
            receivers = [
                {
                    "type": "MERCHANT_ID",
                    "account": str(merchant_id),
                    "amount": int(merchant_amount * 100),
                    "description": f"订单{order.order_no}商户分账",
                }
            ]

            split_result = await pay_client.create_profit_sharing(
                transaction_id=order.wechat_transaction_id,
                receivers=receivers,
            )

            # 更新分账记录状态
            for split in splits:
                split.status = "completed"
                split.completed_at = datetime.now(timezone.utc)
                if split.receiver_type == "merchant":
                    split.wechat_split_id = split_result.get("order_id", "")

            await db.flush()
            logger.info(
                "分账执行成功: order_id=%d, platform=%.2f, merchant=%.2f",
                order_id,
                platform_amount,
                merchant_amount,
            )

        except WeChatPayError as e:
            # 分账失败，记录但不回滚订单
            for split in splits:
                split.status = "failed"
            await db.flush()
            logger.error(
                "微信分账API调用失败: order_id=%d, error=%s",
                order_id,
                e.message,
            )
    else:
        # 非商户订单或缺少交易号，标记为完成（平台全额收入）
        for split in splits:
            split.status = "completed"
            split.completed_at = datetime.now(timezone.utc)
        await db.flush()

    return splits

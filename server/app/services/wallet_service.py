"""数字钱包服务 - 余额管理、流水记录、提现申请

包含：
- get_or_create_wallet: 获取或创建用户钱包
- add_income: 增加收入（分账入账等）
- withdraw: 提现申请（余额检查、冻结、创建提现记录）
- get_transactions: 获取钱包流水记录（分页）
"""

import logging
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet, WalletTransaction

logger = logging.getLogger(__name__)


class WalletServiceError(Exception):
    """钱包服务异常"""

    def __init__(self, message: str, code: str = "WALLET_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


async def get_or_create_wallet(
    db: AsyncSession,
    user_id: int,
) -> Wallet:
    """获取或创建用户钱包

    如果用户尚无钱包，则自动创建一个余额为 0 的钱包。

    Args:
        db: 数据库 Session
        user_id: 用户 ID

    Returns:
        用户的 Wallet 对象
    """
    result = await db.execute(
        select(Wallet).where(Wallet.user_id == user_id)
    )
    wallet = result.scalar_one_or_none()

    if wallet is None:
        wallet = Wallet(
            user_id=user_id,
            balance=Decimal("0.00"),
            frozen_amount=Decimal("0.00"),
            total_income=Decimal("0.00"),
            total_expense=Decimal("0.00"),
        )
        db.add(wallet)
        await db.flush()
        logger.info("创建新钱包: user_id=%d, wallet_id=%d", user_id, wallet.id)

    return wallet


async def add_income(
    db: AsyncSession,
    wallet_id: int,
    amount: Decimal,
    description: str = "",
    reference_id: str | None = None,
) -> WalletTransaction:
    """增加钱包收入

    Args:
        db: 数据库 Session
        wallet_id: 钱包 ID
        amount: 收入金额（正数）
        description: 交易描述
        reference_id: 关联业务单号

    Returns:
        交易记录对象

    Raises:
        WalletServiceError: 钱包不存在或金额无效
    """
    if amount <= 0:
        raise WalletServiceError("收入金额必须大于0", code="INVALID_AMOUNT")

    result = await db.execute(select(Wallet).where(Wallet.id == wallet_id))
    wallet = result.scalar_one_or_none()

    if not wallet:
        raise WalletServiceError("钱包不存在", code="WALLET_NOT_FOUND")

    # 更新余额
    wallet.balance = wallet.balance + amount
    wallet.total_income = wallet.total_income + amount

    # 创建交易记录
    transaction = WalletTransaction(
        wallet_id=wallet_id,
        transaction_type="income",
        amount=amount,
        balance_after=wallet.balance,
        description=description,
        reference_id=reference_id,
    )
    db.add(transaction)
    await db.flush()

    logger.info(
        "钱包收入: wallet_id=%d, amount=%.2f, balance=%.2f",
        wallet_id,
        amount,
        wallet.balance,
    )

    return transaction


async def withdraw(
    db: AsyncSession,
    user_id: int,
    amount: Decimal,
) -> WalletTransaction:
    """提现申请

    检查可用余额是否充足，冻结提现金额，创建提现流水。

    Args:
        db: 数据库 Session
        user_id: 用户 ID
        amount: 提现金额

    Returns:
        提现交易记录

    Raises:
        WalletServiceError: 余额不足或其他错误
    """
    if amount <= 0:
        raise WalletServiceError("提现金额必须大于0", code="INVALID_AMOUNT")

    # 获取钱包
    wallet = await get_or_create_wallet(db, user_id)

    # 检查可用余额（可用余额 = 余额 - 冻结金额）
    available = wallet.balance - wallet.frozen_amount
    if available < amount:
        raise WalletServiceError(
            f"可用余额不足，当前可用: {available}",
            code="INSUFFICIENT_BALANCE",
        )

    # 冻结金额
    wallet.frozen_amount = wallet.frozen_amount + amount
    wallet.total_expense = wallet.total_expense + amount

    # 创建提现交易记录
    transaction = WalletTransaction(
        wallet_id=wallet.id,
        transaction_type="withdrawal",
        amount=-amount,  # 提现为负数
        balance_after=wallet.balance - amount,
        description=f"提现申请 ¥{amount}",
        reference_id=None,
    )
    db.add(transaction)
    await db.flush()

    logger.info(
        "提现申请: user_id=%d, amount=%.2f, frozen=%.2f",
        user_id,
        amount,
        wallet.frozen_amount,
    )

    return transaction


async def get_transactions(
    db: AsyncSession,
    wallet_id: int,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """获取钱包流水记录（分页）

    Args:
        db: 数据库 Session
        wallet_id: 钱包 ID
        page: 页码（从1开始）
        page_size: 每页记录数

    Returns:
        {"items": [...], "total": n, "page": p, "page_size": ps}
    """
    offset = (page - 1) * page_size

    # 查询总数
    count_result = await db.execute(
        select(func.count(WalletTransaction.id)).where(
            WalletTransaction.wallet_id == wallet_id
        )
    )
    total = count_result.scalar() or 0

    # 查询列表
    result = await db.execute(
        select(WalletTransaction)
        .where(WalletTransaction.wallet_id == wallet_id)
        .order_by(WalletTransaction.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    items = result.scalars().all()

    return {
        "items": list(items),
        "total": total,
        "page": page,
        "page_size": page_size,
    }

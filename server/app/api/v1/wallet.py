"""钱包路由 - 余额查询、流水记录、提现申请

Endpoints:
- GET /wallet: 获取钱包信息
- GET /wallet/transactions: 流水记录（分页）
- POST /wallet/withdraw: 发起提现
"""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.wallet import WalletResponse, WalletTransactionResponse
from app.services.wallet_service import (
    WalletServiceError,
    get_or_create_wallet,
    get_transactions,
    withdraw,
)

router = APIRouter()


# ─── Request/Response Models ───────────────────────────────────────


class WithdrawRequest(BaseModel):
    """提现请求"""

    amount: Decimal = Field(..., gt=0, description="提现金额（元）")


class WithdrawResponse(BaseModel):
    """提现响应"""

    transaction_id: int
    amount: Decimal
    balance_after: Decimal
    status: str = "processing"


class TransactionListResponse(BaseModel):
    """流水列表响应"""

    items: list[WalletTransactionResponse]
    total: int
    page: int
    page_size: int


# ─── Endpoints ─────────────────────────────────────────────────────


@router.get("", response_model=WalletResponse)
async def get_wallet_endpoint(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户钱包信息"""
    wallet = await get_or_create_wallet(db, current_user.id)
    return wallet


@router.get("/transactions", response_model=TransactionListResponse)
async def list_transactions_endpoint(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取钱包流水记录"""
    wallet = await get_or_create_wallet(db, current_user.id)

    result = await get_transactions(
        db=db,
        wallet_id=wallet.id,
        page=page,
        page_size=page_size,
    )

    return TransactionListResponse(
        items=result["items"],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.post("/withdraw", response_model=WithdrawResponse, status_code=status.HTTP_201_CREATED)
async def withdraw_endpoint(
    body: WithdrawRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """发起提现申请"""
    try:
        transaction = await withdraw(
            db=db,
            user_id=current_user.id,
            amount=body.amount,
        )
    except WalletServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": e.code, "message": e.message},
        )

    return WithdrawResponse(
        transaction_id=transaction.id,
        amount=abs(transaction.amount),
        balance_after=transaction.balance_after,
        status="processing",
    )

"""管理后台路由"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/dashboard")
async def admin_dashboard():
    """管理仪表盘"""
    # TODO: Task 13.2 实现
    return {"message": "not implemented"}


@router.get("/users")
async def admin_users():
    """用户管理"""
    # TODO: Task 13.3 实现
    return {"message": "not implemented"}


@router.get("/reviews")
async def list_reviews():
    """内容审核列表"""
    # TODO: Task 13.4 实现
    return {"message": "not implemented"}


@router.post("/reviews/{review_id}/approve")
async def approve_review(review_id: int):
    """审核通过"""
    # TODO: Task 13.4 实现
    return {"message": "not implemented"}


@router.post("/reviews/{review_id}/reject")
async def reject_review(review_id: int):
    """审核拒绝"""
    # TODO: Task 13.4 实现
    return {"message": "not implemented"}


@router.get("/finance")
async def admin_finance():
    """财务报表"""
    # TODO: Task 13.5 实现
    return {"message": "not implemented"}


@router.put("/config/elo")
async def update_elo_config():
    """配置 ELO 参数"""
    # TODO: Task 13.6 实现
    return {"message": "not implemented"}

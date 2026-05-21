"""掼友圈帖子路由

提供以下接口：
- GET /posts: 获取帖子列表（分页）
- POST /posts: 发布新帖子
- GET /posts/:id: 获取帖子详情
- DELETE /posts/:id: 删除帖子（仅作者）
- POST /posts/:id/like: 点赞
- DELETE /posts/:id/like: 取消点赞
- GET /posts/:id/comments: 获取评论列表（分页）
- POST /posts/:id/comments: 发表评论
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.content_service import (
    ContentServiceError,
    create_comment,
    create_post,
    delete_post,
    get_comments,
    get_post_detail,
    get_post_feed,
    like_post,
    unlike_post,
)

router = APIRouter()


# ─── Request/Response Schemas ─────────────────────────────────────


class CreatePostRequest(BaseModel):
    """创建帖子请求体"""

    content: str = Field(..., min_length=1, max_length=5000, description="帖子内容")
    images: list[str] = Field(default_factory=list, description="图片 URL 列表")


class CreateCommentRequest(BaseModel):
    """创建评论请求体"""

    content: str = Field(..., min_length=1, max_length=2000, description="评论内容")
    parent_id: int | None = Field(None, description="父评论 ID（回复时使用）")


# ─── 帖子 CRUD (Task 6.1) ────────────────────────────────────────


@router.get("")
async def list_posts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    user_id: int | None = Query(None, description="筛选指定用户的帖子"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取帖子列表（分页）

    按时间倒序返回已发布的帖子，支持按用户筛选。
    每条帖子包含当前用户的点赞状态 (is_liked)。
    """
    result = await get_post_feed(
        page=page,
        page_size=page_size,
        user_id=user_id,
        current_user_id=current_user.id,
        db=db,
    )
    return result


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post_endpoint(
    body: CreatePostRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """发布新帖子

    发布前进行内容审核（敏感词检测），违规内容将被隐藏。
    """
    try:
        post = await create_post(
            user_id=current_user.id,
            content=body.content,
            images=body.images,
            db=db,
        )
    except ContentServiceError as e:
        if e.code == "CONTENT_VIOLATION":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )

    return {
        "id": post.id,
        "user_id": post.user_id,
        "content": post.content,
        "images": post.images or [],
        "like_count": post.like_count,
        "comment_count": post.comment_count,
        "status": post.status,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
    }


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取帖子详情

    返回帖子完整信息，包含当前用户的点赞状态。
    """
    try:
        result = await get_post_detail(
            post_id=post_id,
            current_user_id=current_user.id,
            db=db,
        )
    except ContentServiceError as e:
        if e.code == "POST_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )

    return result


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """删除帖子（仅作者本人可操作）

    执行软删除，将帖子状态设为 'deleted'。
    """
    try:
        await delete_post(
            post_id=post_id,
            user_id=current_user.id,
            db=db,
        )
    except ContentServiceError as e:
        if e.code == "POST_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        if e.code == "PERMISSION_DENIED":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )

    return {"message": "删除成功"}


# ─── 点赞/取消点赞 (Task 6.2) ────────────────────────────────────


@router.post("/{post_id}/like", status_code=status.HTTP_200_OK)
async def like_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """点赞帖子

    Redis Set 缓存 + DB 持久化双写，防止重复点赞。
    """
    try:
        success = await like_post(
            post_id=post_id,
            user_id=current_user.id,
            db=db,
        )
    except ContentServiceError as e:
        if e.code == "POST_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )

    if not success:
        return {"message": "已经点过赞了", "liked": True}

    return {"message": "点赞成功", "liked": True}


@router.delete("/{post_id}/like", status_code=status.HTTP_200_OK)
async def unlike_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """取消点赞

    同步清除 Redis 缓存和 DB 记录。
    """
    try:
        success = await unlike_post(
            post_id=post_id,
            user_id=current_user.id,
            db=db,
        )
    except ContentServiceError as e:
        if e.code == "POST_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )

    if not success:
        return {"message": "尚未点赞", "liked": False}

    return {"message": "取消点赞成功", "liked": False}


# ─── 评论 (Task 6.3) ─────────────────────────────────────────────


@router.get("/{post_id}/comments")
async def list_comments(
    post_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取帖子评论列表（分页）

    返回顶级评论，每条评论包含其回复列表。
    """
    try:
        result = await get_comments(
            post_id=post_id,
            page=page,
            page_size=page_size,
            db=db,
        )
    except ContentServiceError as e:
        if e.code == "POST_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )

    return result


@router.post("/{post_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment_endpoint(
    post_id: int,
    body: CreateCommentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """发表评论

    支持回复（通过 parent_id 指定父评论）。
    评论内容同样进行敏感词审核。
    """
    try:
        comment = await create_comment(
            post_id=post_id,
            user_id=current_user.id,
            content=body.content,
            parent_id=body.parent_id,
            db=db,
        )
    except ContentServiceError as e:
        if e.code == "POST_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        if e.code == "CONTENT_VIOLATION":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message,
            )
        if e.code == "PARENT_COMMENT_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )

    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "content": comment.content,
        "parent_id": comment.parent_id,
        "created_at": comment.created_at,
    }

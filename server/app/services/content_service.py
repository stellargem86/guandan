"""内容服务 - 帖子 CRUD、点赞、评论、内容审核

提供掼友圈核心业务逻辑：
- 帖子发布/分页列表/详情/删除 (Task 6.1)
- 点赞/取消点赞（Redis Set 缓存 + DB 持久化）(Task 6.2)
- 评论/回复/评论列表（支持嵌套）(Task 6.3)
- 内容审核过滤（敏感词检测、先发后审）(Task 6.4)
"""

from sqlalchemy import select, desc, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_manager
from app.models.post import Post, Comment, Like
from app.utils.content_filter import filter_text


class ContentServiceError(Exception):
    """内容服务异常"""

    def __init__(self, message: str, code: str = "CONTENT_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


# ─── 内容审核 (Task 6.4) ─────────────────────────────────────────


def check_content(text: str) -> tuple[bool, list[str]]:
    """检查文本内容是否合规

    Args:
        text: 待检测文本

    Returns:
        (is_clean, violations)
        - is_clean: True 表示内容合规
        - violations: 违规敏感词列表
    """
    return filter_text(text)


# ─── 帖子 CRUD (Task 6.1) ────────────────────────────────────────


async def create_post(
    user_id: int,
    content: str,
    images: list | None = None,
    db: AsyncSession = None,
) -> Post:
    """创建帖子

    发布前进行内容审核，若含敏感词则设置 status='hidden' 并抛出异常。

    Args:
        user_id: 发帖用户 ID
        content: 帖子内容
        images: 图片 URL 列表
        db: 数据库 Session

    Returns:
        创建的 Post 对象

    Raises:
        ContentServiceError: 内容包含敏感词
    """
    if images is None:
        images = []

    # 内容审核
    is_clean, violations = check_content(content)
    if not is_clean:
        # 先发后审：创建帖子但设为 hidden
        post = Post(
            user_id=user_id,
            content=content,
            images=images,
            status="hidden",
        )
        db.add(post)
        await db.flush()
        raise ContentServiceError(
            message=f"内容包含敏感词: {', '.join(violations)}",
            code="CONTENT_VIOLATION",
        )

    post = Post(
        user_id=user_id,
        content=content,
        images=images,
        status="published",
    )
    db.add(post)
    await db.flush()
    return post


async def get_post_feed(
    page: int = 1,
    page_size: int = 20,
    user_id: int | None = None,
    current_user_id: int | None = None,
    db: AsyncSession = None,
) -> dict:
    """获取帖子列表（分页，逆时间排序）

    Args:
        page: 页码 (从 1 开始)
        page_size: 每页数量
        user_id: 可选，筛选特定用户的帖子
        current_user_id: 当前登录用户 ID，用于计算 is_liked
        db: 数据库 Session

    Returns:
        {"items": list[dict], "total": int, "page": int, "page_size": int}
    """
    # 构建查询
    query = select(Post).where(Post.status == "published")
    count_query = select(func.count(Post.id)).where(Post.status == "published")

    if user_id is not None:
        query = query.where(Post.user_id == user_id)
        count_query = count_query.where(Post.user_id == user_id)

    # 总数
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页查询
    offset = (page - 1) * page_size
    query = query.order_by(desc(Post.created_at)).offset(offset).limit(page_size)
    result = await db.execute(query)
    posts = result.scalars().all()

    # 为每个帖子添加 is_liked 标记
    items = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "images": post.images or [],
            "like_count": post.like_count,
            "comment_count": post.comment_count,
            "status": post.status,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "is_liked": False,
        }
        if current_user_id:
            post_dict["is_liked"] = await is_post_liked(
                post_id=post.id, user_id=current_user_id
            )
        items.append(post_dict)

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


async def get_post_detail(
    post_id: int,
    current_user_id: int | None = None,
    db: AsyncSession = None,
) -> dict:
    """获取帖子详情

    Args:
        post_id: 帖子 ID
        current_user_id: 当前用户 ID，用于计算 is_liked
        db: 数据库 Session

    Returns:
        帖子详情字典（含 is_liked 标记）

    Raises:
        ContentServiceError: 帖子不存在
    """
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.status != "deleted")
    )
    post = result.scalar_one_or_none()

    if post is None:
        raise ContentServiceError(
            message="帖子不存在",
            code="POST_NOT_FOUND",
        )

    is_liked = False
    if current_user_id:
        is_liked = await is_post_liked(post_id=post.id, user_id=current_user_id)

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
        "is_liked": is_liked,
    }


async def delete_post(
    post_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> bool:
    """删除帖子（软删除，仅作者本人可操作）

    Args:
        post_id: 帖子 ID
        user_id: 操作用户 ID
        db: 数据库 Session

    Returns:
        True 删除成功

    Raises:
        ContentServiceError: 帖子不存在或无权删除
    """
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.status != "deleted")
    )
    post = result.scalar_one_or_none()

    if post is None:
        raise ContentServiceError(
            message="帖子不存在",
            code="POST_NOT_FOUND",
        )

    if post.user_id != user_id:
        raise ContentServiceError(
            message="无权删除他人帖子",
            code="PERMISSION_DENIED",
        )

    post.status = "deleted"
    await db.flush()
    return True


# ─── 点赞/取消点赞 (Task 6.2) ────────────────────────────────────


async def like_post(
    post_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> bool:
    """点赞帖子

    Redis Set 缓存 + DB 持久化双写。

    Args:
        post_id: 帖子 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        True 点赞成功, False 已经点过赞

    Raises:
        ContentServiceError: 帖子不存在
    """
    # 验证帖子存在
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.status == "published")
    )
    post = result.scalar_one_or_none()
    if post is None:
        raise ContentServiceError(
            message="帖子不存在",
            code="POST_NOT_FOUND",
        )

    # 检查是否已点赞（Redis）
    already_liked = await redis_manager.post_like_check(
        post_id=str(post_id), user_id=str(user_id)
    )
    if already_liked:
        return False

    # 添加到 Redis Set
    await redis_manager.post_like_add(
        post_id=str(post_id), user_id=str(user_id)
    )

    # 创建 DB Like 记录
    like = Like(post_id=post_id, user_id=user_id)
    db.add(like)

    # 递增帖子点赞计数
    post.like_count = (post.like_count or 0) + 1
    await db.flush()

    return True


async def unlike_post(
    post_id: int,
    user_id: int,
    db: AsyncSession = None,
) -> bool:
    """取消点赞

    Redis Set 移除 + DB 删除记录。

    Args:
        post_id: 帖子 ID
        user_id: 用户 ID
        db: 数据库 Session

    Returns:
        True 取消成功, False 未曾点赞

    Raises:
        ContentServiceError: 帖子不存在
    """
    # 验证帖子存在
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.status == "published")
    )
    post = result.scalar_one_or_none()
    if post is None:
        raise ContentServiceError(
            message="帖子不存在",
            code="POST_NOT_FOUND",
        )

    # 从 Redis 移除
    removed = await redis_manager.post_like_remove(
        post_id=str(post_id), user_id=str(user_id)
    )
    if not removed:
        return False

    # 删除 DB 记录
    like_result = await db.execute(
        select(Like).where(
            and_(Like.post_id == post_id, Like.user_id == user_id)
        )
    )
    like = like_result.scalar_one_or_none()
    if like:
        await db.delete(like)

    # 递减帖子点赞计数
    post.like_count = max((post.like_count or 0) - 1, 0)
    await db.flush()

    return True


async def is_post_liked(post_id: int, user_id: int) -> bool:
    """检查用户是否已点赞帖子

    优先查 Redis Set，Redis 不可用时 fallback 到 DB（此处简化仅查 Redis）。

    Args:
        post_id: 帖子 ID
        user_id: 用户 ID

    Returns:
        True 已点赞
    """
    try:
        return await redis_manager.post_like_check(
            post_id=str(post_id), user_id=str(user_id)
        )
    except Exception:
        # Redis 不可用时返回 False（降级策略）
        return False


# ─── 评论 (Task 6.3) ─────────────────────────────────────────────


async def create_comment(
    post_id: int,
    user_id: int,
    content: str,
    parent_id: int | None = None,
    db: AsyncSession = None,
) -> Comment:
    """创建评论

    支持嵌套回复（通过 parent_id 指定父评论）。
    创建后递增帖子评论计数。

    Args:
        post_id: 帖子 ID
        user_id: 评论用户 ID
        content: 评论内容
        parent_id: 父评论 ID（可选，回复时使用）
        db: 数据库 Session

    Returns:
        创建的 Comment 对象

    Raises:
        ContentServiceError: 帖子不存在或内容违规
    """
    # 验证帖子存在
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.status == "published")
    )
    post = result.scalar_one_or_none()
    if post is None:
        raise ContentServiceError(
            message="帖子不存在",
            code="POST_NOT_FOUND",
        )

    # 内容审核
    is_clean, violations = check_content(content)
    if not is_clean:
        raise ContentServiceError(
            message=f"评论包含敏感词: {', '.join(violations)}",
            code="CONTENT_VIOLATION",
        )

    # 验证父评论存在（如果指定）
    if parent_id is not None:
        parent_result = await db.execute(
            select(Comment).where(
                and_(Comment.id == parent_id, Comment.post_id == post_id)
            )
        )
        parent_comment = parent_result.scalar_one_or_none()
        if parent_comment is None:
            raise ContentServiceError(
                message="父评论不存在",
                code="PARENT_COMMENT_NOT_FOUND",
            )

    # 创建评论
    comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=content,
        parent_id=parent_id,
    )
    db.add(comment)

    # 递增帖子评论计数
    post.comment_count = (post.comment_count or 0) + 1
    await db.flush()

    return comment


async def get_comments(
    post_id: int,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = None,
) -> dict:
    """获取帖子评论列表（分页，含嵌套回复）

    返回顶级评论（parent_id 为 None），每条评论附带其回复列表。

    Args:
        post_id: 帖子 ID
        page: 页码
        page_size: 每页数量
        db: 数据库 Session

    Returns:
        {"items": list[dict], "total": int, "page": int, "page_size": int}
    """
    # 验证帖子存在
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.status != "deleted")
    )
    post = result.scalar_one_or_none()
    if post is None:
        raise ContentServiceError(
            message="帖子不存在",
            code="POST_NOT_FOUND",
        )

    # 查询顶级评论总数
    count_query = select(func.count(Comment.id)).where(
        and_(Comment.post_id == post_id, Comment.parent_id.is_(None))
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页查询顶级评论
    offset = (page - 1) * page_size
    top_comments_query = (
        select(Comment)
        .where(and_(Comment.post_id == post_id, Comment.parent_id.is_(None)))
        .order_by(Comment.created_at)
        .offset(offset)
        .limit(page_size)
    )
    top_result = await db.execute(top_comments_query)
    top_comments = top_result.scalars().all()

    # 获取这些顶级评论的回复
    top_ids = [c.id for c in top_comments]
    replies_map: dict[int, list] = {cid: [] for cid in top_ids}

    if top_ids:
        replies_query = (
            select(Comment)
            .where(Comment.parent_id.in_(top_ids))
            .order_by(Comment.created_at)
        )
        replies_result = await db.execute(replies_query)
        replies = replies_result.scalars().all()
        for reply in replies:
            if reply.parent_id in replies_map:
                replies_map[reply.parent_id].append({
                    "id": reply.id,
                    "post_id": reply.post_id,
                    "user_id": reply.user_id,
                    "content": reply.content,
                    "parent_id": reply.parent_id,
                    "created_at": reply.created_at,
                })

    # 构建响应
    items = []
    for comment in top_comments:
        items.append({
            "id": comment.id,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "content": comment.content,
            "parent_id": comment.parent_id,
            "created_at": comment.created_at,
            "replies": replies_map.get(comment.id, []),
        })

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }

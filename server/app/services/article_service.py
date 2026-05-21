"""文章服务 - CRUD 操作、分类列表、阅读量统计

提供以下功能：
- create_article: 创建文章
- get_articles: 分页获取文章列表（可按分类筛选）
- get_article_detail: 获取文章详情（原子递增阅读量）
- update_article: 更新文章
- delete_article: 删除文章
"""

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Article

# 允许的文章分类
VALID_CATEGORIES = ["news", "tutorial", "culture", "strategy"]


class ArticleServiceError(Exception):
    """文章服务异常"""

    def __init__(self, message: str, code: str = "ARTICLE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


async def create_article(
    db: AsyncSession,
    title: str,
    content: str,
    category: str,
    author_id: int | None = None,
    cover_image: str | None = None,
) -> Article:
    """创建文章

    Args:
        db: 数据库 Session
        title: 文章标题
        content: 文章内容
        category: 分类 (news/tutorial/culture/strategy)
        author_id: 作者用户ID
        cover_image: 封面图片URL

    Returns:
        创建的 Article ORM 对象

    Raises:
        ArticleServiceError: 分类无效
    """
    if category not in VALID_CATEGORIES:
        raise ArticleServiceError(
            message=f"无效的分类: {category}，允许的分类: {', '.join(VALID_CATEGORIES)}",
            code="INVALID_CATEGORY",
        )

    article = Article(
        title=title,
        content=content,
        category=category,
        author_id=author_id,
        cover_image=cover_image,
        status="published",
    )
    db.add(article)
    await db.flush()
    return article


async def get_articles(
    db: AsyncSession,
    category: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """分页获取文章列表

    Args:
        db: 数据库 Session
        category: 按分类筛选（可选）
        page: 页码（从1开始）
        page_size: 每页数量

    Returns:
        {
            "items": list[Article],
            "total": int,
            "page": int,
            "page_size": int
        }
    """
    # 构建基础查询
    query = select(Article).where(Article.status == "published")
    count_query = select(func.count(Article.id)).where(Article.status == "published")

    # 按分类筛选
    if category:
        if category not in VALID_CATEGORIES:
            raise ArticleServiceError(
                message=f"无效的分类: {category}",
                code="INVALID_CATEGORY",
            )
        query = query.where(Article.category == category)
        count_query = count_query.where(Article.category == category)

    # 获取总数
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # 分页 + 按创建时间倒序
    offset = (page - 1) * page_size
    query = query.order_by(Article.created_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(query)
    items = list(result.scalars().all())

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


async def get_article_detail(db: AsyncSession, article_id: int) -> Article:
    """获取文章详情并原子递增阅读量

    Args:
        db: 数据库 Session
        article_id: 文章ID

    Returns:
        Article ORM 对象

    Raises:
        ArticleServiceError: 文章不存在
    """
    # 原子递增 view_count
    stmt = (
        update(Article)
        .where(Article.id == article_id)
        .values(view_count=Article.view_count + 1)
    )
    await db.execute(stmt)

    # 查询文章详情
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()

    if article is None:
        raise ArticleServiceError(
            message="文章不存在",
            code="ARTICLE_NOT_FOUND",
        )

    return article


async def update_article(db: AsyncSession, article_id: int, **updates) -> Article:
    """更新文章

    Args:
        db: 数据库 Session
        article_id: 文章ID
        **updates: 要更新的字段

    Returns:
        更新后的 Article ORM 对象

    Raises:
        ArticleServiceError: 文章不存在或分类无效
    """
    # 验证分类
    if "category" in updates and updates["category"] not in VALID_CATEGORIES:
        raise ArticleServiceError(
            message=f"无效的分类: {updates['category']}",
            code="INVALID_CATEGORY",
        )

    # 过滤掉 None 值
    valid_updates = {k: v for k, v in updates.items() if v is not None}

    if not valid_updates:
        raise ArticleServiceError(
            message="没有需要更新的字段",
            code="NO_UPDATES",
        )

    # 执行更新
    stmt = (
        update(Article)
        .where(Article.id == article_id)
        .values(**valid_updates)
    )
    result = await db.execute(stmt)

    if result.rowcount == 0:
        raise ArticleServiceError(
            message="文章不存在",
            code="ARTICLE_NOT_FOUND",
        )

    # 刷新并返回更新后的对象
    await db.flush()
    query_result = await db.execute(select(Article).where(Article.id == article_id))
    article = query_result.scalar_one_or_none()

    return article


async def delete_article(db: AsyncSession, article_id: int) -> bool:
    """删除文章（软删除，设置状态为 hidden）

    Args:
        db: 数据库 Session
        article_id: 文章ID

    Returns:
        是否成功删除

    Raises:
        ArticleServiceError: 文章不存在
    """
    stmt = (
        update(Article)
        .where(Article.id == article_id)
        .values(status="hidden")
    )
    result = await db.execute(stmt)

    if result.rowcount == 0:
        raise ArticleServiceError(
            message="文章不存在",
            code="ARTICLE_NOT_FOUND",
        )

    return True

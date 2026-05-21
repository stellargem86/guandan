"""资讯文章路由 - 文章 CRUD、分类列表、阅读量统计

提供以下接口：
- GET /articles: 分页获取文章列表（可按分类筛选）
- POST /articles: 创建文章（仅管理员）
- GET /articles/:id: 获取文章详情（递增阅读量）
- PUT /articles/:id: 更新文章（仅管理员）
- DELETE /articles/:id: 删除文章（仅管理员）

文章分类：news（官方新闻）、tutorial（新手教程）、culture（文化文章）、strategy（策略技巧）
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.content import (
    ArticleCreate,
    ArticleResponse,
    ArticleUpdate,
)
from app.services.article_service import (
    ArticleServiceError,
    create_article,
    delete_article,
    get_article_detail,
    get_articles,
    update_article,
)

router = APIRouter()


@router.get("", response_model=dict)
async def list_articles(
    category: str | None = Query(None, description="文章分类筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """获取文章列表（分页）

    支持按分类筛选，按创建时间倒序排列。
    分类：news / tutorial / culture / strategy
    """
    try:
        result = await get_articles(
            db=db, category=category, page=page, page_size=page_size
        )
    except ArticleServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    return {
        "items": [ArticleResponse.model_validate(item) for item in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
    }


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article_endpoint(
    body: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """创建文章（仅管理员）

    创建新的资讯文章，作者为当前管理员或指定的 author_id。
    """
    try:
        article = await create_article(
            db=db,
            title=body.title,
            content=body.content,
            category=body.category,
            author_id=body.author_id or current_user.id,
            cover_image=body.cover_image,
        )
    except ArticleServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    return ArticleResponse.model_validate(article)


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article_endpoint(
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取文章详情

    每次访问自动递增阅读量。
    """
    try:
        article = await get_article_detail(db=db, article_id=article_id)
    except ArticleServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    return ArticleResponse.model_validate(article)


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article_endpoint(
    article_id: int,
    body: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """更新文章（仅管理员）"""
    try:
        article = await update_article(
            db=db,
            article_id=article_id,
            **body.model_dump(exclude_unset=True),
        )
    except ArticleServiceError as e:
        if e.code == "ARTICLE_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    return ArticleResponse.model_validate(article)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_endpoint(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """删除文章（仅管理员，软删除）"""
    try:
        await delete_article(db=db, article_id=article_id)
    except ArticleServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

"""资讯 & 广告 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Article Schemas
# ============================================================


class ArticleBase(BaseModel):
    """文章基础字段"""

    title: str = Field(..., max_length=256, description="文章标题")
    content: str = Field(..., description="文章内容")
    cover_image: str | None = Field(None, max_length=512, description="封面图片")
    category: str = Field(..., max_length=30, description="分类")


class ArticleCreate(ArticleBase):
    """创建文章"""

    author_id: int | None = Field(None, description="作者用户ID")


class ArticleUpdate(BaseModel):
    """更新文章（所有字段可选）"""

    title: str | None = Field(None, max_length=256)
    content: str | None = None
    cover_image: str | None = Field(None, max_length=512)
    category: str | None = Field(None, max_length=30)
    status: str | None = Field(None, max_length=20)


class ArticleInDB(ArticleBase):
    """数据库中的文章"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int | None = None
    view_count: int = 0
    status: str = "published"
    created_at: datetime
    updated_at: datetime


class ArticleResponse(ArticleInDB):
    """文章 API 响应"""

    pass


# ============================================================
# Advertisement Schemas
# ============================================================


class AdvertisementBase(BaseModel):
    """广告基础字段"""

    title: str = Field(..., max_length=128, description="广告标题")
    image_url: str = Field(..., max_length=512, description="广告图片URL")
    link_url: str | None = Field(None, max_length=512, description="点击跳转链接")
    position: str = Field(..., max_length=30, description="投放位置")
    start_date: datetime | None = Field(None, description="投放开始时间")
    end_date: datetime | None = Field(None, description="投放结束时间")


class AdvertisementCreate(AdvertisementBase):
    """创建广告"""

    pass


class AdvertisementUpdate(BaseModel):
    """更新广告（所有字段可选）"""

    title: str | None = Field(None, max_length=128)
    image_url: str | None = Field(None, max_length=512)
    link_url: str | None = Field(None, max_length=512)
    position: str | None = Field(None, max_length=30)
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: str | None = Field(None, max_length=20)


class AdvertisementInDB(AdvertisementBase):
    """数据库中的广告"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    impressions: int = 0
    clicks: int = 0
    status: str = "active"
    created_at: datetime
    updated_at: datetime


class AdvertisementResponse(AdvertisementInDB):
    """广告 API 响应"""

    pass

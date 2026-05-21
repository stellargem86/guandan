"""帖子 & 评论 & 点赞 Pydantic Schemas

提供 Base / Create / Update / InDB / Response 模式用于 API 数据验证。
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Post Schemas
# ============================================================


class PostBase(BaseModel):
    """帖子基础字段"""

    content: str = Field(..., description="帖子内容")
    images: list | None = Field(default_factory=list, description="图片数组")


class PostCreate(PostBase):
    """创建帖子"""

    user_id: int = Field(..., description="发帖用户ID")


class PostUpdate(BaseModel):
    """更新帖子（所有字段可选）"""

    content: str | None = None
    images: list | None = None
    status: str | None = Field(None, max_length=20)


class PostInDB(PostBase):
    """数据库中的帖子"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    like_count: int = 0
    comment_count: int = 0
    status: str = "published"
    created_at: datetime
    updated_at: datetime


class PostResponse(PostInDB):
    """帖子 API 响应"""

    pass


# ============================================================
# Comment Schemas
# ============================================================


class CommentBase(BaseModel):
    """评论基础字段"""

    content: str = Field(..., description="评论内容")
    parent_id: int | None = Field(None, description="父评论ID（嵌套回复）")


class CommentCreate(CommentBase):
    """创建评论"""

    post_id: int = Field(..., description="关联帖子ID")
    user_id: int = Field(..., description="评论用户ID")


class CommentUpdate(BaseModel):
    """更新评论（所有字段可选）"""

    content: str | None = None


class CommentInDB(CommentBase):
    """数据库中的评论"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    user_id: int
    created_at: datetime


class CommentResponse(CommentInDB):
    """评论 API 响应"""

    pass


# ============================================================
# Like Schemas
# ============================================================


class LikeBase(BaseModel):
    """点赞基础字段"""

    post_id: int = Field(..., description="关联帖子ID")
    user_id: int = Field(..., description="点赞用户ID")


class LikeCreate(LikeBase):
    """创建点赞"""

    pass


class LikeInDB(LikeBase):
    """数据库中的点赞"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class LikeResponse(LikeInDB):
    """点赞 API 响应"""

    pass

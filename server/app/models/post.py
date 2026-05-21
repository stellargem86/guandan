"""帖子模型 (Posts) + 评论模型 (Comments) + 点赞模型 (Likes)

对应 DDL: posts 表, comments 表, likes 表
帖子为掼友圈的核心内容；评论支持嵌套回复；点赞唯一约束防止重复。
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Post(Base):
    """帖子表 ORM 模型"""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="发帖用户"
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False, comment="帖子内容"
    )
    images: Mapped[dict | None] = mapped_column(
        JSONB, server_default="'[]'", comment="图片数组"
    )
    like_count: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="点赞数"
    )
    comment_count: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="评论数"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="published",
        comment="状态: published / hidden / deleted"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post", lazy="selectin"
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like", back_populates="post", lazy="selectin"
    )

    __table_args__ = (
        Index("idx_posts_user", "user_id"),
        Index("idx_posts_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, user_id={self.user_id})>"


class Comment(Base):
    """评论表 ORM 模型"""

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="关联帖子"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="评论用户"
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False, comment="评论内容"
    )
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="父评论ID（嵌套回复）"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    replies: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="parent", lazy="selectin"
    )
    parent: Mapped["Comment | None"] = relationship(
        "Comment", back_populates="replies", remote_side="Comment.id"
    )

    __table_args__ = (
        Index("idx_comments_post", "post_id"),
        Index("idx_comments_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, post_id={self.post_id})>"


class Like(Base):
    """点赞表 ORM 模型"""

    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="关联帖子"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="点赞用户"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("post_id", "user_id", name="uq_likes_post_user"),
        Index("idx_likes_post", "post_id"),
        Index("idx_likes_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<Like(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"

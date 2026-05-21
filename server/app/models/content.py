"""资讯模型 (Articles) + 广告模型 (Advertisements)

对应 DDL: articles 表, advertisements 表
资讯管理文章发布与分类；广告管理投放位置与统计。
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Article(Base):
    """资讯文章表 ORM 模型"""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        String(256), nullable=False, comment="文章标题"
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False, comment="文章内容"
    )
    cover_image: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="封面图片"
    )
    category: Mapped[str] = mapped_column(
        String(30), nullable=False, comment="分类: news / tutorial / strategy / interview"
    )
    author_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="作者用户ID"
    )
    view_count: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="浏览量"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="published",
        comment="状态: published / draft / hidden"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        Index("idx_articles_category", "category"),
        Index("idx_articles_status", "status"),
        Index("idx_articles_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title={self.title})>"


class Advertisement(Base):
    """广告表 ORM 模型"""

    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        String(128), nullable=False, comment="广告标题"
    )
    image_url: Mapped[str] = mapped_column(
        String(512), nullable=False, comment="广告图片URL"
    )
    link_url: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="点击跳转链接"
    )
    position: Mapped[str] = mapped_column(
        String(30), nullable=False, comment="投放位置: home_banner / feed_card / event_banner"
    )
    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="投放开始时间"
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="投放结束时间"
    )
    impressions: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="曝光次数"
    )
    clicks: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="点击次数"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="active",
        comment="状态: active / paused / expired"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        Index("idx_advertisements_position", "position"),
        Index("idx_advertisements_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<Advertisement(id={self.id}, title={self.title}, position={self.position})>"

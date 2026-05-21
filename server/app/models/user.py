"""用户模型 (Users)

对应 DDL: users 表
包含平台用户的基本信息、微信绑定信息、角色与状态管理。
"""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """用户表 ORM 模型"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    platform_id: Mapped[str] = mapped_column(
        String(32), unique=True, nullable=False, comment="平台唯一 ID"
    )
    wechat_openid: Mapped[str | None] = mapped_column(
        String(128), unique=True, nullable=True, comment="微信 OpenID"
    )
    wechat_unionid: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="微信 UnionID"
    )
    nickname: Mapped[str] = mapped_column(
        String(64), nullable=False, comment="用户昵称"
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="头像 URL"
    )
    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="手机号"
    )
    industry: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="所属行业（用于组局匹配）"
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="user",
        comment="用户角色: user / merchant / organizer / admin"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="active",
        comment="账号状态: active / banned / inactive"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        Index("idx_users_wechat_openid", "wechat_openid"),
        Index("idx_users_platform_id", "platform_id"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, platform_id={self.platform_id}, nickname={self.nickname})>"

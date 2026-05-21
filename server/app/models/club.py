"""俱乐部模型 (Clubs) + 成员模型 (Club Members) + 活动模型 (Club Activities)

对应 DDL: clubs 表, club_members 表, club_activities 表
俱乐部管理创建与状态；成员管理加入与角色；活动管理俱乐部内部活动。
"""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Club(Base):
    """俱乐部表 ORM 模型"""

    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="创建者用户ID"
    )
    name: Mapped[str] = mapped_column(
        String(128), nullable=False, comment="俱乐部名称"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="俱乐部描述"
    )
    avatar_url: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="俱乐部头像"
    )
    region: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="所在地区"
    )
    membership_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), server_default="0.00", comment="会员费"
    )
    max_members: Mapped[int] = mapped_column(
        Integer, server_default="200", comment="最大成员数"
    )
    current_members: Mapped[int] = mapped_column(
        Integer, server_default="1", comment="当前成员数"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="active",
        comment="状态: active / suspended / disbanded"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    members: Mapped[list["ClubMember"]] = relationship(
        "ClubMember", back_populates="club", lazy="selectin"
    )
    activities: Mapped[list["ClubActivity"]] = relationship(
        "ClubActivity", back_populates="club", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Club(id={self.id}, name={self.name})>"


class ClubMember(Base):
    """俱乐部成员表 ORM 模型"""

    __tablename__ = "club_members"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    club_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="所属俱乐部"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="成员用户ID"
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="member",
        comment="角色: owner / admin / member"
    )
    order_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="关联订单（会员费）"
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="active",
        comment="状态: active / left / banned"
    )

    # Relationships
    club: Mapped["Club"] = relationship("Club", back_populates="members")

    __table_args__ = (
        UniqueConstraint("club_id", "user_id", name="uq_club_members_club_user"),
        Index("idx_club_members_club", "club_id"),
        Index("idx_club_members_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<ClubMember(id={self.id}, club_id={self.club_id}, user_id={self.user_id})>"


class ClubActivity(Base):
    """俱乐部活动表 ORM 模型"""

    __tablename__ = "club_activities"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    club_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="所属俱乐部"
    )
    creator_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="创建者用户ID"
    )
    title: Mapped[str] = mapped_column(
        String(128), nullable=False, comment="活动标题"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="活动描述"
    )
    activity_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="活动时间"
    )
    location: Mapped[str | None] = mapped_column(
        String(256), nullable=True, comment="活动地点"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="upcoming",
        comment="状态: upcoming / ongoing / completed / cancelled"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    club: Mapped["Club"] = relationship("Club", back_populates="activities")

    __table_args__ = (
        Index("idx_club_activities_club", "club_id"),
    )

    def __repr__(self) -> str:
        return f"<ClubActivity(id={self.id}, title={self.title})>"

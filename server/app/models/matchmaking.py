"""组局模型 (Matchmaking Requests) + 参与者模型 (Matchmaking Participants)

对应 DDL: matchmaking_requests 表, matchmaking_participants 表
一键组局管理创建与状态；参与者跟踪加入/取消和押金。
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
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MatchmakingRequest(Base):
    """组局请求表 ORM 模型"""

    __tablename__ = "matchmaking_requests"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="创建者用户ID"
    )
    title: Mapped[str] = mapped_column(
        String(128), nullable=False, comment="组局标题"
    )
    scheduled_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="预定时间"
    )
    location: Mapped[str | None] = mapped_column(
        String(256), nullable=True, comment="地点"
    )
    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True, comment="纬度"
    )
    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7), nullable=True, comment="经度"
    )
    min_rank: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="最低段位要求"
    )
    max_rank: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="最高段位要求"
    )
    industry_tag: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="行业标签"
    )
    max_players: Mapped[int] = mapped_column(
        Integer, server_default="4", comment="最大人数"
    )
    current_players: Mapped[int] = mapped_column(
        Integer, server_default="1", comment="当前人数"
    )
    deposit_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), server_default="0.00", comment="押金金额"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="open",
        comment="状态: open / full / completed / cancelled"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    participants: Mapped[list["MatchmakingParticipant"]] = relationship(
        "MatchmakingParticipant", back_populates="request", lazy="selectin"
    )

    __table_args__ = (
        Index("idx_matchmaking_requests_creator", "creator_id"),
        Index("idx_matchmaking_requests_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<MatchmakingRequest(id={self.id}, title={self.title}, status={self.status})>"


class MatchmakingParticipant(Base):
    """组局参与者表 ORM 模型"""

    __tablename__ = "matchmaking_participants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    request_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="关联组局请求"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="参与者用户ID"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="joined",
        comment="状态: joined / cancelled"
    )
    deposit_order_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="押金订单ID"
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="取消时间"
    )

    # Relationships
    request: Mapped["MatchmakingRequest"] = relationship(
        "MatchmakingRequest", back_populates="participants"
    )

    __table_args__ = (
        UniqueConstraint("request_id", "user_id", name="uq_matchmaking_participants_request_user"),
        Index("idx_matchmaking_participants_request", "request_id"),
        Index("idx_matchmaking_participants_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<MatchmakingParticipant(id={self.id}, request_id={self.request_id}, user_id={self.user_id})>"

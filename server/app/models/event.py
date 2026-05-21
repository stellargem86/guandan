"""赛事模型 (Events) + 赛事报名模型 (Event Registrations)

对应 DDL: events 表, event_registrations 表
赛事管理发布、报名与签到；报名记录跟踪用户参赛状态。
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


class Event(Base):
    """赛事表 ORM 模型"""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    organizer_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="组织者用户ID"
    )
    title: Mapped[str] = mapped_column(
        String(128), nullable=False, comment="赛事标题"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="赛事描述"
    )
    cover_image: Mapped[str | None] = mapped_column(
        String(512), nullable=True, comment="封面图片"
    )
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="赛事日期"
    )
    location: Mapped[str | None] = mapped_column(
        String(256), nullable=True, comment="赛事地点"
    )
    entry_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), server_default="0.00", comment="报名费"
    )
    max_capacity: Mapped[int] = mapped_column(
        Integer, server_default="100", comment="最大参赛人数"
    )
    current_registrations: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="当前报名人数"
    )
    rules: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="赛事规则"
    )
    cancel_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="取消报名截止时间"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="upcoming",
        comment="状态: upcoming / ongoing / completed / cancelled"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    registrations: Mapped[list["EventRegistration"]] = relationship(
        "EventRegistration", back_populates="event", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, title={self.title})>"


class EventRegistration(Base):
    """赛事报名表 ORM 模型"""

    __tablename__ = "event_registrations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="关联赛事"
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="报名用户"
    )
    order_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="关联订单"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="registered",
        comment="状态: registered / cancelled / checked_in"
    )
    checked_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="签到时间"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    event: Mapped["Event"] = relationship("Event", back_populates="registrations")

    __table_args__ = (
        UniqueConstraint("event_id", "user_id", name="uq_event_registrations_event_user"),
        Index("idx_event_registrations_event", "event_id"),
        Index("idx_event_registrations_user", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<EventRegistration(id={self.id}, event_id={self.event_id}, user_id={self.user_id})>"

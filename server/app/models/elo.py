"""ELO 积分模型 (ELO Scores) + 对局记录模型 (Match Results)

对应 DDL: elo_scores 表, match_results 表
ELO 积分管理用户天梯分数与段位；对局记录跟踪每场比赛的分数变化。
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
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EloScore(Base):
    """ELO 积分表 ORM 模型"""

    __tablename__ = "elo_scores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="所属用户"
    )
    score: Mapped[int] = mapped_column(
        Integer, server_default="1200", comment="ELO 积分"
    )
    tier: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="bronze",
        comment="段位: bronze / silver / gold / platinum / diamond"
    )
    total_matches: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="总对局数"
    )
    wins: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="胜场数"
    )
    losses: Mapped[int] = mapped_column(
        Integer, server_default="0", comment="败场数"
    )
    win_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 4), server_default="0.0000", comment="胜率"
    )
    k_factor: Mapped[int] = mapped_column(
        Integer, server_default="32", comment="K因子: 新手32, 成熟玩家16"
    )
    region: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="地区（用于地区排行）"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_elo_scores_user_id"),
        Index("idx_elo_scores_score", "score"),
        Index("idx_elo_scores_region", "region", "score"),
    )

    def __repr__(self) -> str:
        return f"<EloScore(id={self.id}, user_id={self.user_id}, score={self.score}, tier={self.tier})>"


class MatchResult(Base):
    """对局记录表 ORM 模型"""

    __tablename__ = "match_results"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="关联赛事（可为空，表示非赛事对局）"
    )
    winner_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="胜者用户ID"
    )
    loser_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, comment="败者用户ID"
    )
    winner_score_before: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="胜者赛前分数"
    )
    winner_score_after: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="胜者赛后分数"
    )
    loser_score_before: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="败者赛前分数"
    )
    loser_score_after: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="败者赛后分数"
    )
    recorded_by: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True, comment="记录者用户ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("idx_match_results_event", "event_id"),
        Index("idx_match_results_winner", "winner_id"),
        Index("idx_match_results_loser", "loser_id"),
    )

    def __repr__(self) -> str:
        return f"<MatchResult(id={self.id}, winner_id={self.winner_id}, loser_id={self.loser_id})>"

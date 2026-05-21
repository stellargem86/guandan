"""create all core tables

Revision ID: 001_create_all_core_tables
Revises:
Create Date: 2024-01-01 00:00:00.000000

Creates all core platform tables:
- users, elo_scores, merchants, dining_packages
- orders, revenue_splits, wallets, wallet_transactions
- matchmaking_requests, matchmaking_participants
- events, event_registrations
- clubs, club_members, club_activities
- posts, comments, likes
- match_results, articles, advertisements
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001_create_all_core_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # =============================================
    # 1. users
    # =============================================
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("platform_id", sa.String(32), nullable=False),
        sa.Column("wechat_openid", sa.String(128), nullable=True),
        sa.Column("wechat_unionid", sa.String(128), nullable=True),
        sa.Column("nickname", sa.String(64), nullable=False),
        sa.Column("avatar_url", sa.String(512), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("industry", sa.String(64), nullable=True),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform_id"),
        sa.UniqueConstraint("wechat_openid"),
    )
    op.create_index("idx_users_wechat_openid", "users", ["wechat_openid"])
    op.create_index("idx_users_platform_id", "users", ["platform_id"])

    # =============================================
    # 2. elo_scores
    # =============================================
    op.create_table(
        "elo_scores",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("score", sa.Integer(), server_default="1200"),
        sa.Column("tier", sa.String(20), nullable=False, server_default="bronze"),
        sa.Column("total_matches", sa.Integer(), server_default="0"),
        sa.Column("wins", sa.Integer(), server_default="0"),
        sa.Column("losses", sa.Integer(), server_default="0"),
        sa.Column("win_rate", sa.Numeric(5, 4), server_default="0.0000"),
        sa.Column("k_factor", sa.Integer(), server_default="32"),
        sa.Column("region", sa.String(64), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("user_id", name="uq_elo_scores_user_id"),
    )
    op.create_index("idx_elo_scores_score", "elo_scores", ["score"])
    op.create_index("idx_elo_scores_region", "elo_scores", ["region", "score"])

    # =============================================
    # 3. merchants
    # =============================================
    op.create_table(
        "merchants",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("address", sa.String(256), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("geohash", sa.String(12), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("rating", sa.Numeric(3, 2), server_default="0.00"),
        sa.Column("cover_image", sa.String(512), nullable=True),
        sa.Column("photos", postgresql.JSONB(), server_default="'[]'"),
        sa.Column("business_hours", sa.String(128), nullable=True),
        sa.Column("bank_account", sa.String(64), nullable=True),
        sa.Column("commission_rate", sa.Numeric(4, 3), server_default="0.100"),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("idx_merchants_geohash", "merchants", ["geohash"])
    op.create_index("idx_merchants_status", "merchants", ["status"])

    # =============================================
    # 4. dining_packages
    # =============================================
    op.create_table(
        "dining_packages",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("merchant_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("original_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("cover_image", sa.String(512), nullable=True),
        sa.Column("validity_days", sa.Integer(), server_default="30"),
        sa.Column("inventory", sa.Integer(), server_default="999"),
        sa.Column("sold_count", sa.Integer(), server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["merchant_id"], ["merchants.id"]),
    )
    op.create_index("idx_dining_packages_merchant", "dining_packages", ["merchant_id", "status"])

    # =============================================
    # 5. orders
    # =============================================
    op.create_table(
        "orders",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("order_no", sa.String(64), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("order_type", sa.String(30), nullable=False),
        sa.Column("target_id", sa.BigInteger(), nullable=True),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("wechat_transaction_id", sa.String(64), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("refunded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verification_code", sa.String(64), nullable=True),
        sa.Column("verification_qr_url", sa.String(512), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("idempotency_key", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_no"),
        sa.UniqueConstraint("idempotency_key"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("idx_orders_user", "orders", ["user_id", "created_at"])
    op.create_index("idx_orders_order_no", "orders", ["order_no"])
    op.create_index("idx_orders_status", "orders", ["status"])
    op.create_index(
        "idx_orders_verification", "orders", ["verification_code"],
        postgresql_where=sa.text("verification_code IS NOT NULL"),
    )

    # =============================================
    # 6. revenue_splits
    # =============================================
    op.create_table(
        "revenue_splits",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.BigInteger(), nullable=False),
        sa.Column("receiver_type", sa.String(20), nullable=False),
        sa.Column("receiver_id", sa.BigInteger(), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("ratio", sa.Numeric(4, 3), nullable=False),
        sa.Column("wechat_split_id", sa.String(64), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
    )
    op.create_index("idx_revenue_splits_order", "revenue_splits", ["order_id"])
    op.create_index("idx_revenue_splits_receiver", "revenue_splits", ["receiver_type", "receiver_id"])

    # =============================================
    # 7. wallets
    # =============================================
    op.create_table(
        "wallets",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("balance", sa.Numeric(12, 2), server_default="0.00"),
        sa.Column("frozen_amount", sa.Numeric(12, 2), server_default="0.00"),
        sa.Column("total_income", sa.Numeric(12, 2), server_default="0.00"),
        sa.Column("total_expense", sa.Numeric(12, 2), server_default="0.00"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("user_id", name="uq_wallets_user_id"),
    )

    # =============================================
    # 8. wallet_transactions
    # =============================================
    op.create_table(
        "wallet_transactions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("wallet_id", sa.BigInteger(), nullable=False),
        sa.Column("transaction_type", sa.String(30), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("balance_after", sa.Numeric(12, 2), nullable=False),
        sa.Column("description", sa.String(256), nullable=True),
        sa.Column("reference_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["wallet_id"], ["wallets.id"]),
    )

    # =============================================
    # 9. matchmaking_requests
    # =============================================
    op.create_table(
        "matchmaking_requests",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("creator_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("scheduled_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(256), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("min_rank", sa.String(20), nullable=True),
        sa.Column("max_rank", sa.String(20), nullable=True),
        sa.Column("industry_tag", sa.String(64), nullable=True),
        sa.Column("max_players", sa.Integer(), server_default="4"),
        sa.Column("current_players", sa.Integer(), server_default="1"),
        sa.Column("deposit_amount", sa.Numeric(10, 2), server_default="0.00"),
        sa.Column("status", sa.String(20), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
    )
    op.create_index("idx_matchmaking_requests_creator", "matchmaking_requests", ["creator_id"])
    op.create_index("idx_matchmaking_requests_status", "matchmaking_requests", ["status"])

    # =============================================
    # 10. matchmaking_participants
    # =============================================
    op.create_table(
        "matchmaking_participants",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("request_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="joined"),
        sa.Column("deposit_order_id", sa.BigInteger(), nullable=True),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["request_id"], ["matchmaking_requests.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["deposit_order_id"], ["orders.id"]),
        sa.UniqueConstraint("request_id", "user_id", name="uq_matchmaking_participants_request_user"),
    )
    op.create_index("idx_matchmaking_participants_request", "matchmaking_participants", ["request_id"])
    op.create_index("idx_matchmaking_participants_user", "matchmaking_participants", ["user_id"])

    # =============================================
    # 11. events
    # =============================================
    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("organizer_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("cover_image", sa.String(512), nullable=True),
        sa.Column("event_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(256), nullable=True),
        sa.Column("entry_fee", sa.Numeric(10, 2), server_default="0.00"),
        sa.Column("max_capacity", sa.Integer(), server_default="100"),
        sa.Column("current_registrations", sa.Integer(), server_default="0"),
        sa.Column("rules", sa.Text(), nullable=True),
        sa.Column("cancel_deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="upcoming"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["organizer_id"], ["users.id"]),
    )

    # =============================================
    # 12. event_registrations
    # =============================================
    op.create_table(
        "event_registrations",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("order_id", sa.BigInteger(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="registered"),
        sa.Column("checked_in_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.UniqueConstraint("event_id", "user_id", name="uq_event_registrations_event_user"),
    )
    op.create_index("idx_event_registrations_event", "event_registrations", ["event_id"])
    op.create_index("idx_event_registrations_user", "event_registrations", ["user_id"])

    # =============================================
    # 13. clubs
    # =============================================
    op.create_table(
        "clubs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("owner_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("avatar_url", sa.String(512), nullable=True),
        sa.Column("region", sa.String(64), nullable=True),
        sa.Column("membership_fee", sa.Numeric(10, 2), server_default="0.00"),
        sa.Column("max_members", sa.Integer(), server_default="200"),
        sa.Column("current_members", sa.Integer(), server_default="1"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
    )

    # =============================================
    # 14. club_members
    # =============================================
    op.create_table(
        "club_members",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("club_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="member"),
        sa.Column("order_id", sa.BigInteger(), nullable=True),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.UniqueConstraint("club_id", "user_id", name="uq_club_members_club_user"),
    )
    op.create_index("idx_club_members_club", "club_members", ["club_id"])
    op.create_index("idx_club_members_user", "club_members", ["user_id"])

    # =============================================
    # 15. club_activities
    # =============================================
    op.create_table(
        "club_activities",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("club_id", sa.BigInteger(), nullable=False),
        sa.Column("creator_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("activity_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("location", sa.String(256), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="upcoming"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["club_id"], ["clubs.id"]),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
    )
    op.create_index("idx_club_activities_club", "club_activities", ["club_id"])

    # =============================================
    # 16. posts
    # =============================================
    op.create_table(
        "posts",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("images", postgresql.JSONB(), server_default="'[]'"),
        sa.Column("like_count", sa.Integer(), server_default="0"),
        sa.Column("comment_count", sa.Integer(), server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="published"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )
    op.create_index("idx_posts_user", "posts", ["user_id"])
    op.create_index("idx_posts_created", "posts", ["created_at"])

    # =============================================
    # 17. comments
    # =============================================
    op.create_table(
        "comments",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("parent_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["parent_id"], ["comments.id"]),
    )
    op.create_index("idx_comments_post", "comments", ["post_id"])
    op.create_index("idx_comments_user", "comments", ["user_id"])

    # =============================================
    # 18. likes
    # =============================================
    op.create_table(
        "likes",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("post_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint("post_id", "user_id", name="uq_likes_post_user"),
    )
    op.create_index("idx_likes_post", "likes", ["post_id"])
    op.create_index("idx_likes_user", "likes", ["user_id"])

    # =============================================
    # 19. match_results
    # =============================================
    op.create_table(
        "match_results",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.BigInteger(), nullable=True),
        sa.Column("winner_id", sa.BigInteger(), nullable=False),
        sa.Column("loser_id", sa.BigInteger(), nullable=False),
        sa.Column("winner_score_before", sa.Integer(), nullable=False),
        sa.Column("winner_score_after", sa.Integer(), nullable=False),
        sa.Column("loser_score_before", sa.Integer(), nullable=False),
        sa.Column("loser_score_after", sa.Integer(), nullable=False),
        sa.Column("recorded_by", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["winner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["loser_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["recorded_by"], ["users.id"]),
    )
    op.create_index("idx_match_results_event", "match_results", ["event_id"])
    op.create_index("idx_match_results_winner", "match_results", ["winner_id"])
    op.create_index("idx_match_results_loser", "match_results", ["loser_id"])

    # =============================================
    # 20. articles
    # =============================================
    op.create_table(
        "articles",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("cover_image", sa.String(512), nullable=True),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("author_id", sa.BigInteger(), nullable=True),
        sa.Column("view_count", sa.Integer(), server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="published"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
    )
    op.create_index("idx_articles_category", "articles", ["category"])
    op.create_index("idx_articles_status", "articles", ["status"])
    op.create_index("idx_articles_created", "articles", ["created_at"])

    # =============================================
    # 21. advertisements
    # =============================================
    op.create_table(
        "advertisements",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("image_url", sa.String(512), nullable=False),
        sa.Column("link_url", sa.String(512), nullable=True),
        sa.Column("position", sa.String(30), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("impressions", sa.Integer(), server_default="0"),
        sa.Column("clicks", sa.Integer(), server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_advertisements_position", "advertisements", ["position"])
    op.create_index("idx_advertisements_status", "advertisements", ["status"])


def downgrade() -> None:
    op.drop_table("advertisements")
    op.drop_table("articles")
    op.drop_table("match_results")
    op.drop_table("likes")
    op.drop_table("comments")
    op.drop_table("posts")
    op.drop_table("club_activities")
    op.drop_table("club_members")
    op.drop_table("clubs")
    op.drop_table("event_registrations")
    op.drop_table("events")
    op.drop_table("matchmaking_participants")
    op.drop_table("matchmaking_requests")
    op.drop_table("wallet_transactions")
    op.drop_table("wallets")
    op.drop_table("revenue_splits")
    op.drop_table("orders")
    op.drop_table("dining_packages")
    op.drop_table("merchants")
    op.drop_table("elo_scores")
    op.drop_table("users")

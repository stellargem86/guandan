"""create users table

Revision ID: 001_create_users
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001_create_users"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("platform_id", sa.String(32), nullable=False, comment="平台唯一 ID"),
        sa.Column("wechat_openid", sa.String(128), nullable=True, comment="微信 OpenID"),
        sa.Column("wechat_unionid", sa.String(128), nullable=True, comment="微信 UnionID"),
        sa.Column("nickname", sa.String(64), nullable=False, comment="用户昵称"),
        sa.Column("avatar_url", sa.String(512), nullable=True, comment="头像 URL"),
        sa.Column("phone", sa.String(20), nullable=True, comment="手机号"),
        sa.Column("industry", sa.String(64), nullable=True, comment="所属行业（用于组局匹配）"),
        sa.Column(
            "role", sa.String(20), nullable=False, server_default="user",
            comment="用户角色: user / merchant / organizer / admin",
        ),
        sa.Column(
            "status", sa.String(20), nullable=False, server_default="active",
            comment="账号状态: active / banned / inactive",
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform_id"),
        sa.UniqueConstraint("wechat_openid"),
    )

    # 创建索引
    op.create_index("idx_users_wechat_openid", "users", ["wechat_openid"])
    op.create_index("idx_users_platform_id", "users", ["platform_id"])


def downgrade() -> None:
    op.drop_index("idx_users_platform_id", table_name="users")
    op.drop_index("idx_users_wechat_openid", table_name="users")
    op.drop_table("users")

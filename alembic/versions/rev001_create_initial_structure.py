"""create initial structure

Revision ID: rev001
Revises: rev000
Create Date: 2022-11-29 02:16:34.093120

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "rev001"
down_revision = "rev000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "characters",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("server_version", sa.Integer),
        sa.Column("timestamp", sa.TIMESTAMP, nullable=False),
        sa.Column("character_type", sa.String(50), nullable=False),
        sa.Column("scale_type", sa.String(50), nullable=False),
        sa.Column("size_x", sa.Float, nullable=False),
        sa.Column("size_y", sa.Float, nullable=False),
        sa.Column("size_z", sa.Float, nullable=False),
    )
    op.create_table(
        "users",
        sa.Column(
            "user_id", sa.Integer, primary_key=True, nullable=False, autoincrement=False
        ),
        sa.Column("last_modified", sa.TIMESTAMP, nullable=False),
        sa.Column("name", sa.String(50), nullable=True),
    )
    op.create_table(
        "users_history",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("timestamp", sa.TIMESTAMP, nullable=False),
        sa.Column("name", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("users_history")
    op.drop_table("users")
    op.drop_table("characters")

"""Add missing structure

Revision ID: rev002
Revises: rev001
Create Date: 2022-12-3 02:31:34.093120

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "rev002"
down_revision = "rev001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "characters", "id", new_column_name="character_id", existing_type=sa.Integer
    )

    op.create_table(
        "positions",
        sa.Column("position_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("server_id", sa.BINARY, nullable=False),
        sa.Column("server_version", sa.Integer, nullable=False),
        sa.Column("timestamp", sa.TIMESTAMP, nullable=False),
        sa.Column("position_x", sa.Float, nullable=False),
        sa.Column("position_y_model", sa.Float, nullable=False),
        sa.Column("position_y_ground", sa.Float, nullable=False),
        sa.Column("position_z", sa.Float, nullable=False),
        sa.Column("rotation_x", sa.Float, nullable=False),
        sa.Column("rotation_y", sa.Float, nullable=False),
        sa.Column("rotation_z", sa.Float, nullable=False),
        sa.Column("velocity_x", sa.Float, nullable=False),
        sa.Column("velocity_y", sa.Float, nullable=False),
        sa.Column("velocity_z", sa.Float, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("character_id", sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        None,
        "positions",
        "users",
        ["user_id"],
        ["user_id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        None,
        "positions",
        "characters",
        ["character_id"],
        ["character_id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_characters_positions", "positions", type_="foreignkey")
    op.drop_constraint("fk_users_positions", "positions", type_="foreignkey")
    op.drop_table("positions")
    op.alter_column(
        "characters", "character_id", new_column_name="id", existing_type=sa.Integer
    )

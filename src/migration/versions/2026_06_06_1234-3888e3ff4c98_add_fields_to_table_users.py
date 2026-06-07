"""add fields to table users

Revision ID: 3888e3ff4c98
Revises: a678f8ecede3
Create Date: 2026-06-06 12:34:37.517373

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3888e3ff4c98"
down_revision: str | Sequence[str] | None = "a678f8ecede3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_name", sa.String(), nullable=False))
    op.add_column("users", sa.Column("first_name", sa.String(), nullable=False))
    op.add_column("users", sa.Column("middle_name", sa.String(), nullable=True))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "is_active")
    op.drop_column("users", "middle_name")
    op.drop_column("users", "first_name")
    op.drop_column("users", "last_name")

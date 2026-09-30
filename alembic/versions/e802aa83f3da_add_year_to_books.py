"""add year to books

Revision ID: e802aa83f3da
Revises: 9ab673e127c0
Create Date: 2026-08-07 14:23:29.434327

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e802aa83f3da"
down_revision: Union[str, Sequence[str], None] = "9ab673e127c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column("books", sa.Column("year", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("books", "year")

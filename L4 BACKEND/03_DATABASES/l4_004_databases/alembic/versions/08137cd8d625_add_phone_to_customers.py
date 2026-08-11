

"""add phone to customers

Revision ID: 08137cd8d625
Revises: 
Create Date: 2026-08-12 01:20:06.488334

"""
from typing import Sequence, Union


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08137cd8d625'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add phone column."""

    op.add_column(
        "customers",
        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=True
        )
    )


def downgrade() -> None:
    """Remove phone column."""

    op.drop_column(
        "customers",
        "phone"
    )

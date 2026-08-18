"""empty init

Revision ID: 418cb1de2795
Revises: 
Create Date: 2026-08-19 02:31:50.726718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '418cb1de2795'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

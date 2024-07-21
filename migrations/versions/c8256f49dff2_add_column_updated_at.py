"""add column updated_at

Revision ID: c8256f49dff2
Revises: 7537de3cd399
Create Date: 2024-06-26 20:39:56.758224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision: str = 'c8256f49dff2'
down_revision: Union[str, None] = '7537de3cd399'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), server_default=str(datetime.now()), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'updated_at')

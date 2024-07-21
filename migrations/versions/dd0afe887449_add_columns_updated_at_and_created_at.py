"""add columns updated_at and created_at

Revision ID: dd0afe887449
Revises: 9721bd0668cd
Create Date: 2024-07-21 10:19:06.538565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision: str = 'dd0afe887449'
down_revision: Union[str, None] = '9721bd0668cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('todos', sa.Column('updated_at', sa.DateTime(), server_default=str(datetime.now()), nullable=False))
    op.add_column('todos', sa.Column('created_at', sa.DateTime(), server_default=str(datetime.now()), nullable=False))


def downgrade() -> None:
    op.drop_column('todos', 'created_at')
    op.drop_column('todos', 'updated_at')

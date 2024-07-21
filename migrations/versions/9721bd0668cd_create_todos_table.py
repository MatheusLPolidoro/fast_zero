"""create todos table

Revision ID: 9721bd0668cd
Revises: c8256f49dff2
Create Date: 2024-07-20 18:46:37.382905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9721bd0668cd'
down_revision: Union[str, None] = 'c8256f49dff2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('state', sa.Enum('draft', 'todo', 'doing', 'done', 'trash', name='todostate'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('todos')

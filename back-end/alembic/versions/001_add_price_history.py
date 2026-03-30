"""add price_history table

Revision ID: 001_price_history
Revises:
Create Date: 2026-03-30
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_price_history'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'price_history',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('tender_items.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('source_store', sa.String(100), nullable=False),
        sa.Column('product_title', sa.String(500), nullable=True),
        sa.Column('product_url', sa.String(1000), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), index=True),
    )


def downgrade() -> None:
    op.drop_table('price_history')

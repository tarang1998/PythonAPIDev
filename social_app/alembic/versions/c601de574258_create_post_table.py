"""Create post table

Revision ID: c601de574258
Revises: 
Create Date: 2025-03-26 02:45:02.851045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c601de574258'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False,primary_key=True), 
        sa.Column('title', sa.String(), nullable=False)
    )    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass

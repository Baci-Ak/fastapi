"""add foreign-key to posts table

Revision ID: 59ed1d73b902
Revises: 5416086a9a66
Create Date: 2025-08-28 10:18:32.320531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59ed1d73b902'
down_revision: Union[str, Sequence[str], None] = '5416086a9a66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table= 'users',
                          local_cols= ['user_id'], remote_cols= ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass

"""Optional dates in Basket

Revision ID: 83c72ddcc7d7
Revises: cce20988af3f
Create Date: 2023-10-30 00:32:58.908875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '83c72ddcc7d7'
down_revision: Union[str, None] = 'cce20988af3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('basket', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('basket', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('basket', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('basket', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###

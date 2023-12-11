"""Init

Revision ID: ba252031558f
Revises: aae33552fe2b
Create Date: 2023-11-18 22:28:05.691725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba252031558f'
down_revision: Union[str, None] = 'aae33552fe2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'test_field')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('test_field', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
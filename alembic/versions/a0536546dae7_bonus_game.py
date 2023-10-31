"""Bonus game +

Revision ID: a0536546dae7
Revises: 60d28428631a
Create Date: 2023-10-30 02:49:20.812221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0536546dae7'
down_revision: Union[str, None] = '60d28428631a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'book', 'game', ['bonus_game_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'book', type_='foreignkey')
    # ### end Alembic commands ###

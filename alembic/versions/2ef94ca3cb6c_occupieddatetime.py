"""OccupiedDateTime +

Revision ID: 2ef94ca3cb6c
Revises: a0536546dae7
Create Date: 2023-10-31 17:02:37.446870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ef94ca3cb6c'
down_revision: Union[str, None] = 'a0536546dae7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('occupieddatetime',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('game_to_book_id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['game_to_book_id'], ['gametobook.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('occupieddatetime')
    # ### end Alembic commands ###

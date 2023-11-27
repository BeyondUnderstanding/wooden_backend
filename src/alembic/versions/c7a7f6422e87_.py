"""empty message

Revision ID: c7a7f6422e87
Revises: ba252031558f
Create Date: 2023-11-27 00:20:37.052705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7a7f6422e87'
down_revision: Union[str, None] = 'ba252031558f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('occupieddatetime', 'game_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('occupieddatetime', 'game_to_book_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('occupieddatetime', 'game_to_book_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('occupieddatetime', 'game_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_table('config')
    # ### end Alembic commands ###

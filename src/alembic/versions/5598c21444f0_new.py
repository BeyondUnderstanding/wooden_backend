"""New

Revision ID: 5598c21444f0
Revises: 
Create Date: 2023-10-24 18:18:45.804941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5598c21444f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('login', sa.String(length=30), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_table('game',
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('client_name', sa.String(), nullable=False),
    sa.Column('client_phone', sa.String(), nullable=False),
    sa.Column('is_payed', sa.Boolean(), nullable=True),
    sa.Column('is_refunded', sa.Boolean(), nullable=True),
    sa.Column('is_canceled', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gameattribute',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('is_main', sa.Boolean(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('image',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    op.drop_table('gameattribute')
    op.drop_table('book')
    op.drop_table('game')
    op.drop_table('admin')
    # ### end Alembic commands ###
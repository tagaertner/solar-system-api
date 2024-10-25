"""adds Planet model

Revision ID: 4294dced1c4c
Revises: c72d9c7a8b07
Create Date: 2024-10-25 13:10:11.729115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4294dced1c4c'
down_revision = 'c72d9c7a8b07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('moon', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('planets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.INTEGER(), sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), autoincrement=True, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('moon', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='planets_pkey')
    )
    op.drop_table('planet')
    # ### end Alembic commands ###
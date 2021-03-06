"""empty message

Revision ID: e900acc6e0f5
Revises: 
Create Date: 2020-08-12 17:12:15.137881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e900acc6e0f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('newstype',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('type_name', sa.String(length=11), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=16), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('icon', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('new',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['newstype.id'], ),
    sa.ForeignKeyConstraint(['u_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('new')
    op.drop_table('user')
    op.drop_table('newstype')
    # ### end Alembic commands ###

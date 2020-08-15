"""empty message

Revision ID: 7c3169deaef1
Revises: c4085670d890
Create Date: 2020-08-13 15:19:07.099603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c3169deaef1'
down_revision = 'c4085670d890'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reply',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('content', sa.String(length=255), nullable=False),
    sa.Column('love_num', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'comment', 'new', ['news_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'new', 'user', ['u_id'], ['id'])
    op.create_foreign_key(None, 'new', 'newstype', ['type_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'new', type_='foreignkey')
    op.drop_constraint(None, 'new', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_table('reply')
    # ### end Alembic commands ###

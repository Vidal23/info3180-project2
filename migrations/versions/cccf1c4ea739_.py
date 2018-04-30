"""empty message

Revision ID: cccf1c4ea739
Revises: 
Create Date: 2018-04-27 04:01:59.732518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cccf1c4ea739'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('firstname', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.Column('biography', sa.String(length=255), nullable=True),
    sa.Column('profile_photo', sa.String(length=80), nullable=True),
    sa.Column('joined_on', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('photo', sa.String(length=80), nullable=True),
    sa.Column('caption', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('posts')
    op.drop_table('follows')
    op.drop_table('users')
    # ### end Alembic commands ###

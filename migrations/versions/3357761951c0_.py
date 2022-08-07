"""empty message

Revision ID: 3357761951c0
Revises: 
Create Date: 2022-08-06 15:58:45.234835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3357761951c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('g_auth_verify', sa.Boolean(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('empty__template',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_added', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_added'], ['user.token'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meme',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('image_id', sa.String(length=300), nullable=True),
    sa.Column('caption', sa.String(length=200), nullable=True),
    sa.Column('user_token', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_token'], ['user.token'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meme')
    op.drop_table('empty__template')
    op.drop_table('user')
    # ### end Alembic commands ###

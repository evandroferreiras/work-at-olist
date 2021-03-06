"""empty message

Revision ID: 0b1713891fdd
Revises: 
Create Date: 2018-10-06 21:06:26.140596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b1713891fdd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('example',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('example')
    # ### end Alembic commands ###

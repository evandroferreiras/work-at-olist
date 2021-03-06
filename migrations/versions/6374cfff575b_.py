"""empty message

Revision ID: 6374cfff575b
Revises: 0b1713891fdd
Create Date: 2018-10-09 22:54:55.927062

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, String

from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '6374cfff575b'
down_revision = '0b1713891fdd'
branch_labels = None
depends_on = None

call_detail_type = table('call_detail_type',
                         column('id', Integer),
                         column('description', String))


def __insert_values_call_detail_value():
    op.bulk_insert(call_detail_type,
                   [
                       {
                           'id': 1,
                           'description': 'start'
                       },
                       {
                           'id': 2,
                           'description': 'end'
                       }
                   ])


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('call',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('source_phone', sa.String(
                        length=11), nullable=True),
                    sa.Column('destination_phone', sa.String(
                        length=11), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('call_detail_type',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.String(
                        length=120), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('call_detail',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('detail_type_id', sa.Integer(), nullable=False),
                    sa.Column('date_added', sa.DateTime(), nullable=False),
                    sa.Column('call_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['call_id'], ['call.id'], ),
                    sa.ForeignKeyConstraint(['detail_type_id'], [
                                            'call_detail_type.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_table('example')
    __insert_values_call_detail_value()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('example',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('description', sa.VARCHAR(length=120),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='example_pkey')
                    )
    op.drop_table('call_detail')
    op.drop_table('call_detail_type')
    op.drop_table('call')
    # ### end Alembic commands ###

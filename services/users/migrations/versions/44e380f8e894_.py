"""empty message

Revision ID: 44e380f8e894
Revises: 0a0f57635d25
Create Date: 2019-08-25 18:44:10.140660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44e380f8e894'
down_revision = '0a0f57635d25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

"""empty message

Revision ID: 94eb878d0caa
Revises: 
Create Date: 2019-07-13 18:00:00.900785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94eb878d0caa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['username'])
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###

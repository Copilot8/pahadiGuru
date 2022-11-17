"""pic

Revision ID: 6518f9542f04
Revises: 46e386963616
Create Date: 2022-11-16 17:30:17.987555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6518f9542f04'
down_revision = '46e386963616'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_pic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'profile_pic')
    # ### end Alembic commands ###
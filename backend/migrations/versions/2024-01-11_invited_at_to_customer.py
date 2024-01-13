"""invited_at to customer

Revision ID: 4d16a7d7a677
Revises: b266714bcb19
Create Date: 2024-01-11 20:00:34.129695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d16a7d7a677'
down_revision = 'b266714bcb19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('invited_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'invited_at')
    # ### end Alembic commands ###

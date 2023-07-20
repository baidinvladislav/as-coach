"""exercises on training cascade delete

Revision ID: 04dea0019dc0
Revises: 8e9438cf8eed
Create Date: 2023-07-18 09:54:06.236479

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04dea0019dc0'
down_revision = '8e9438cf8eed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('exercisesontraining', 'training_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('exercisesontraining', 'exercise_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.drop_constraint('exercisesontraining_training_id_fkey', 'exercisesontraining', type_='foreignkey')
    op.drop_constraint('exercisesontraining_exercise_id_fkey', 'exercisesontraining', type_='foreignkey')
    op.create_foreign_key(None, 'exercisesontraining', 'training', ['training_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'exercisesontraining', 'exercise', ['exercise_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exercisesontraining', type_='foreignkey')
    op.drop_constraint(None, 'exercisesontraining', type_='foreignkey')
    op.create_foreign_key('exercisesontraining_exercise_id_fkey', 'exercisesontraining', 'exercise', ['exercise_id'], ['id'])
    op.create_foreign_key('exercisesontraining_training_id_fkey', 'exercisesontraining', 'training', ['training_id'], ['id'])
    op.alter_column('exercisesontraining', 'exercise_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('exercisesontraining', 'training_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###

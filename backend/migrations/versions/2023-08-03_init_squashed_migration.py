"""init squashed migration

Revision ID: 7ca6bc8f8e69
Revises: 
Create Date: 2023-08-03 10:23:18.069270

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7ca6bc8f8e69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coach',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('photo_path', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coach_id'), 'coach', ['id'], unique=False)
    op.create_table('diet',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('proteins', sa.Integer(), nullable=False),
    sa.Column('fats', sa.Integer(), nullable=False),
    sa.Column('carbs', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diet_id'), 'diet', ['id'], unique=False)
    op.create_table('musclegroup',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_musclegroup_id'), 'musclegroup', ['id'], unique=False)
    op.create_table('customer',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='gender'), nullable=True),
    sa.Column('coach_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('photo_path', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['coach_id'], ['coach.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_id'), 'customer', ['id'], unique=False)
    op.create_table('exercise',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('coach_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('muscle_group_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['coach_id'], ['coach.id'], ),
    sa.ForeignKeyConstraint(['muscle_group_id'], ['musclegroup.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_id'), 'exercise', ['id'], unique=False)
    op.create_table('trainingplan',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('set_rest', sa.Integer(), nullable=True),
    sa.Column('exercise_rest', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trainingplan_id'), 'trainingplan', ['id'], unique=False)
    op.create_table('dietontrainingplan',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('diet_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('training_plan_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['diet_id'], ['diet.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['training_plan_id'], ['trainingplan.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dietontrainingplan_id'), 'dietontrainingplan', ['id'], unique=False)
    op.create_table('training',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('training_plan_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['training_plan_id'], ['trainingplan.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_id'), 'training', ['id'], unique=False)
    op.create_table('exercisesontraining',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('training_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('exercise_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('sets', sa.JSON(), nullable=True),
    sa.Column('superset_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ordering', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['training_id'], ['training.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercisesontraining_id'), 'exercisesontraining', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_exercisesontraining_id'), table_name='exercisesontraining')
    op.drop_table('exercisesontraining')
    op.drop_index(op.f('ix_training_id'), table_name='training')
    op.drop_table('training')
    op.drop_index(op.f('ix_dietontrainingplan_id'), table_name='dietontrainingplan')
    op.drop_table('dietontrainingplan')
    op.drop_index(op.f('ix_trainingplan_id'), table_name='trainingplan')
    op.drop_table('trainingplan')
    op.drop_index(op.f('ix_exercise_id'), table_name='exercise')
    op.drop_table('exercise')
    op.drop_index(op.f('ix_customer_id'), table_name='customer')
    op.drop_table('customer')
    op.drop_index(op.f('ix_musclegroup_id'), table_name='musclegroup')
    op.drop_table('musclegroup')
    op.drop_index(op.f('ix_diet_id'), table_name='diet')
    op.drop_table('diet')
    op.drop_index(op.f('ix_coach_id'), table_name='coach')
    op.drop_table('coach')
    # ### end Alembic commands ###

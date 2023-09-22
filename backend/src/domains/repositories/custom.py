"""
Stores custom repositories for interaction with data storage
"""

from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from src import (
    Coach,
    Customer,
    TrainingPlan,
    Diet,
    DietOnTrainingPlan,
    Training,
    Exercise,
    ExercisesOnTraining,
    MuscleGroup
)
from src.domains.repositories.sqlalchemy import SQLAlchemyRepository


class CoachRepository(SQLAlchemyRepository):
    """
    Access to Coach storage
    """
    model = Coach


class CustomerRepository(SQLAlchemyRepository):
    """
    Access to Customer storage
    """
    model = Customer


class TrainingPlanRepository(SQLAlchemyRepository):
    """
    Access to TrainingPlan storage
    """
    model = TrainingPlan


class TrainingRepository(SQLAlchemyRepository):
    """
    Access to Training storage
    """
    model = Training


class DietRepository(SQLAlchemyRepository):
    """
    Access to Diet storage
    """
    model = Diet


class DietOnTrainingPlanRepository(SQLAlchemyRepository):
    """
    Access to DietOnTrainingPlan storage
    """
    model = DietOnTrainingPlan


class ExerciseRepository(SQLAlchemyRepository):
    """
    Access to Exercise storage
    """
    model = Exercise

    async def filter(self, filters: dict, foreign_keys: list = None, sub_queries: list = None):
        """
        Provides list of exercises for specified coach

        Args:
            filters: filters to look for coach
            foreign_keys: list of foreign keys fields
            sub_queries: list of fields for sub queries
        """
        result = await self.session.execute(
            select(Exercise).where(
                or_(
                    Exercise.coach_id.is_(None),
                    Exercise.coach_id == filters["coach_id"]
                )
            ).options(
                selectinload(Exercise.muscle_group)
            )
        )

        instances = result.scalars().all()
        return instances


class ExercisesOnTrainingRepository(SQLAlchemyRepository):
    """
    Access to ExercisesOnTraining storage
    """
    model = ExercisesOnTraining

    async def filter(self, filters: dict, foreign_keys: list = None, sub_queries: list = None):
        result = await self.session.execute(
            select(self.model).order_by(self.model.ordering).where(
                self.model.training_id.in_(filters["training_ids"])
            )
        )

        instances = result.scalars().all()
        return instances


class MuscleGroupRepository(SQLAlchemyRepository):
    """
    Access to MuscleGroup storage
    """
    model = MuscleGroup

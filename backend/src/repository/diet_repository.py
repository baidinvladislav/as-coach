from uuid import UUID
from datetime import date

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src import Diet, DietDays, TrainingPlan
from src.schemas.diet_dto import DailyDietDtoSchema


class DietRepository:
    async def insert_diet_templates(self, uow: AsyncSession, training_plan_id: UUID, diets: list) -> list[UUID]:
        diet_orm = [
            Diet(
                total_proteins=diet.proteins,
                total_fats=diet.fats,
                total_carbs=diet.carbs,
                total_calories=diet.calories,
                training_plan_id=training_plan_id,
            )
            for diet in diets
        ]

        uow.add_all(diet_orm)
        await uow.flush()

        return diet_orm

    async def create_daily_diet(
        self,
        uow: AsyncSession,
        template_diet_id: UUID,
        specific_day: date,
    ) -> DailyDietDtoSchema | None:
        query = await uow.execute(
            select(Diet).filter(Diet.id == template_diet_id)
        )
        template_diet = query.scalars().first()

        daily_diet = DietDays(
            date=specific_day,
            diet=template_diet,
            diet_id=template_diet.id,
            breakfast={
                "total_calories": 0,
                "total_proteins": 0,
                "total_fats": 0,
                "total_carbs": 0,
                "products": [],
            },
            lunch={
                "total_calories": 0,
                "total_proteins": 0,
                "total_fats": 0,
                "total_carbs": 0,
                "products": [],
            },
            dinner={
                "total_calories": 0,
                "total_proteins": 0,
                "total_fats": 0,
                "total_carbs": 0,
                "products": [],
            },
            snacks={
                "total_calories": 0,
                "total_proteins": 0,
                "total_fats": 0,
                "total_carbs": 0,
                "products": [],
            },

        )

        uow.add(daily_diet)
        await uow.flush()

        return DailyDietDtoSchema.from_daily_diet_fact(daily_diet)

    async def get_daily_diet_by_training_plan_date_range(
        self, uow: AsyncSession, customer_id: UUID, specific_day: date
    ) -> DailyDietDtoSchema | None:
        query = (
            select(Diet)
            .join(TrainingPlan, Diet.training_plan_id == TrainingPlan.id)
            .options(selectinload(Diet.diet_days))
            .where(
                and_(
                    TrainingPlan.customer_id == customer_id,
                    TrainingPlan.start_date <= specific_day,
                    TrainingPlan.end_date >= specific_day,
                )
            )
        )
        result = await uow.execute(query)
        recommended_diet_by_coach = result.scalar_one_or_none()
        return DailyDietDtoSchema.from_recommended_diet(recommended_diet_by_coach, specific_day)

    async def get_daily_diet_by_id(
        self,
        uow: AsyncSession,
        daily_diet_id: UUID,
    ) -> DailyDietDtoSchema | None:
        query = (
            select(DietDays)
            .options(selectinload(DietDays.diet))
            .where(DietDays.id == daily_diet_id)
        )

        result = await uow.execute(query)
        diet_day = result.scalar_one_or_none()

        if diet_day is None:
            return None

        return DailyDietDtoSchema.from_daily_diet_fact(diet_day)

    async def update_daily_diet_meal(
        self,
        uow: AsyncSession,
        updated_daily_diet: DailyDietDtoSchema,
        meal_type: str,
        updated_meal: dict,
    ) -> DailyDietDtoSchema | None:
        column_to_update = getattr(DietDays, meal_type)

        stmt = (
            update(DietDays)
            .where(DietDays.id == updated_daily_diet.diet_day_id)
            .values({column_to_update: updated_meal})
            .returning(DietDays.id)
        )

        result = await uow.execute(stmt)
        updated_record_id = result.scalar_one_or_none()
        await uow.commit()

        if updated_record_id is None:
            return None

        query = (
            select(DietDays)
            .options(joinedload(DietDays.diet))
            .where(DietDays.id == updated_record_id)
        )

        result = await uow.execute(query)
        daily_diet_fact = result.scalar_one_or_none()

        if daily_diet_fact is None:
            return None

        return DailyDietDtoSchema.from_daily_diet_fact(daily_diet_fact)

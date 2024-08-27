import json
from uuid import UUID
from datetime import date, datetime

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src import Diet, DietDays, TrainingPlan
from src.schemas.diet_dto import DailyDietDtoSchema


class DietRepository:
    async def create_diets(self, uow: AsyncSession, training_plan_id: UUID, diets: list) -> list[UUID]:
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

    async def get_daily_diet(
        self, uow: AsyncSession, customer_id: UUID, specific_day: date
    ) -> DailyDietDtoSchema | None:
        query = (
            select(
                Diet
            ).join(
                TrainingPlan, Diet.training_plan_id == TrainingPlan.id,
            ).where(
                and_(
                    TrainingPlan.customer_id == customer_id,
                    TrainingPlan.start_date <= specific_day,
                    TrainingPlan.end_date >= specific_day
                )
            )
        )
        result = await uow.execute(query)
        recommended_diet_by_coach = result.scalar_one_or_none()

        if recommended_diet_by_coach is None:
            return None

        return DailyDietDtoSchema.from_diet(recommended_diet_by_coach, specific_day)

    async def add_product_to_customer_fact(
        self,
        uow: AsyncSession,
        diet_id: UUID,
        specific_day: str,
        meal_type: str,
        product_id: UUID,
        product_amount: int,
    ):
        query = (
            select(DietDays)
            .where(
                and_(
                    DietDays.diet_id == diet_id,
                    DietDays.date == datetime.strptime(specific_day, "%Y-%m-%d").date(),
                )
            )
        )

        result = await uow.execute(query)
        diet_day = result.scalar_one_or_none()

        if diet_day is None:
            return None

        current_json = getattr(diet_day, meal_type)
        current_json[str(product_id)] = product_amount

        update_stmt = (
            update(DietDays)
            .where(DietDays.id == diet_day.id)
            .values(**{meal_type: json.dumps(current_json)})
            .returning(DietDays.id)
        )

        update_result = await uow.execute(update_stmt)
        updated_row = update_result.fetchone()

        await uow.commit()
        return updated_row

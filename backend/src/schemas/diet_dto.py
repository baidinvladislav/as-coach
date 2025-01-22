import logging
from uuid import UUID
from datetime import date

from pydantic import BaseModel

from src import Diet, DietDays

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DietDtoSchema(BaseModel):
    """This created by coach as template"""

    id: UUID
    total_proteins: int
    total_fats: int
    total_carbs: int
    total_calories: int

    class Config:
        orm_mode = True


class DailyNutrients(BaseModel):
    """
    Nutrition plan/fact model.
    Inherited by Meal and DailyDiet.
    """

    total_calories: int
    consumed_calories: int

    total_proteins: int
    consumed_proteins: int

    total_fats: int
    consumed_fats: int

    total_carbs: int
    consumed_carbs: int


class DailyDietDtoSchema(BaseModel):
    """
    This diet fork for customer.
    This record keeps nutrition customer results.
    """
    date: date

    template_diet_id: UUID | None
    total_calories: int
    total_proteins: int
    total_fats: int
    total_carbs: int

    diet_day_id: UUID | None
    consumed_calories: int
    consumed_proteins: int
    consumed_fats: int
    consumed_carbs: int

    breakfast: dict
    lunch: dict
    dinner: dict
    snacks: dict

    @classmethod
    def from_daily_diet_fact(cls, daily_diet_fact: DietDays) -> "DailyDietDtoSchema":
        meals = [
            daily_diet_fact.breakfast, daily_diet_fact.lunch, daily_diet_fact.dinner, daily_diet_fact.snacks,
        ]

        return DailyDietDtoSchema(
            # recommend amount by coach
            template_diet_id=daily_diet_fact.diet_id,
            total_calories=daily_diet_fact.diet.total_calories,
            total_proteins=daily_diet_fact.diet.total_proteins,
            total_fats=daily_diet_fact.diet.total_fats,
            total_carbs=daily_diet_fact.diet.total_carbs,

            # fact amount
            diet_day_id=daily_diet_fact.id,
            date=daily_diet_fact.date,

            consumed_calories=sum(meal["total_calories"] for meal in meals),
            consumed_proteins=sum(meal["total_proteins"] for meal in meals),
            consumed_fats=sum(meal["total_fats"] for meal in meals),
            consumed_carbs=sum(meal["total_carbs"] for meal in meals),

            breakfast=daily_diet_fact.breakfast,
            lunch=daily_diet_fact.lunch,
            dinner=daily_diet_fact.dinner,
            snacks=daily_diet_fact.snacks,
        )

    @classmethod
    def create_empty_diet(cls, template_diet: Diet | None, specific_day: date) -> "DailyDietDtoSchema":
        return DailyDietDtoSchema(
            # recommend amount by coach
            template_diet_id=None if template_diet is None else template_diet.id,
            total_calories=0 if template_diet is None else template_diet.total_calories,
            total_proteins=0 if template_diet is None else template_diet.total_proteins,
            total_fats=0 if template_diet is None else template_diet.total_fats,
            total_carbs=0 if template_diet is None else template_diet.total_carbs,

            # fact amount
            diet_day_id=None,
            date=specific_day,

            consumed_calories=0,
            consumed_proteins=0,
            consumed_fats=0,
            consumed_carbs=0,

            breakfast={},
            lunch={},
            dinner={},
            snacks={},
        )

    @classmethod
    def from_recommended_diet(cls, template_diet: Diet | None, specific_day: date) -> "DailyDietDtoSchema":
        if template_diet is None:
            # the customer doesn't have any diet from coach for the date
            logger.info(
                f"customer.doesn't.have.any.diet.for.date, details=template_diet: {template_diet}, specific_day: {date}"
            )
            return cls.create_empty_diet(None, specific_day)

        customer_fact_days = template_diet.diet_days
        if not customer_fact_days:
            # the customer hasn't logged any days from the diet
            logger.info(
                f"customer.hasn't.logged.any.diet.days, details=template_diet: {template_diet}, specific_day: {date}"
            )
            return cls.create_empty_diet(template_diet, specific_day)

        specific_day_fact = next((day for day in customer_fact_days if day.date == specific_day), None)

        if specific_day_fact is None:
            # the customer hasn't logged the requested day
            logger.info(
                f"customer.hasn't.logged.requested.day, details=template_diet: {template_diet}, specific_day: {date}"
            )
            return cls.create_empty_diet(template_diet, specific_day)

        meals = [
            specific_day_fact.breakfast, specific_day_fact.lunch, specific_day_fact.dinner, specific_day_fact.snacks
        ]

        return DailyDietDtoSchema(
            # recommend amount by coach
            template_diet_id=template_diet.id,
            total_calories=template_diet.total_calories,
            total_proteins=template_diet.total_proteins,
            total_fats=template_diet.total_fats,
            total_carbs=template_diet.total_carbs,

            # fact amount
            diet_day_id=specific_day_fact.id,
            date=specific_day_fact.date,

            consumed_calories=sum(meal["total_calories"] for meal in meals),
            consumed_proteins=sum(meal["total_proteins"] for meal in meals),
            consumed_fats=sum(meal["total_fats"] for meal in meals),
            consumed_carbs=sum(meal["total_carbs"] for meal in meals),

            breakfast=specific_day_fact.breakfast,
            lunch=specific_day_fact.lunch,
            dinner=specific_day_fact.dinner,
            snacks=specific_day_fact.snacks,
        )

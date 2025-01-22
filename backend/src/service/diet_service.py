import logging
from datetime import date
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.presentation.schemas.nutrition_schema import MealType, ProductAddInDiet
from src.presentation.schemas.training_plan_schema import DietIn
from src.repository.diet_repository import DietRepository
from src.schemas.diet_dto import DailyDietDtoSchema
from src.service.calories_calculator_service import CaloriesCalculatorService
from src.service.product_service import ProductService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class DietService:
    def __init__(
        self,
        diet_repository: DietRepository,
        calories_calculator_service: CaloriesCalculatorService,
        product_service: ProductService,
    ) -> None:
        self.diet_repository = diet_repository
        self.calories_calculator_service = calories_calculator_service
        self.product_service = product_service

    async def _actualize_daily_diet_fact(
        self,
        updating_daily_diet: DailyDietDtoSchema,
        meal_type: MealType,
        product_list: list[dict],
    ) -> tuple[DailyDietDtoSchema, dict]:
        updating_meal = getattr(updating_daily_diet, meal_type.value)
        for item in product_list:
            item["calories"] *= item["amount"] / 100
            item["proteins"] *= item["amount"] / 100
            item["fats"] *= item["amount"] / 100
            item["carbs"] *= item["amount"] / 100

            updating_daily_diet.consumed_calories += item["calories"]
            updating_daily_diet.consumed_proteins += item["proteins"]
            updating_daily_diet.consumed_fats += item["fats"]
            updating_daily_diet.consumed_carbs += item["carbs"]

            updating_meal["total_calories"] += item["calories"]
            updating_meal["total_proteins"] += item["proteins"]
            updating_meal["total_fats"] += item["fats"]
            updating_meal["total_carbs"] += item["carbs"]

            updating_meal["products"].append(item)

        return updating_daily_diet, updating_meal

    async def put_product_to_diet_meal(
        self,
        uow: AsyncSession,
        daily_diet_id: UUID,
        meal_type: MealType,
        adding_products_data: list[ProductAddInDiet],
    ) -> DailyDietDtoSchema | None:
        products_full_info = await self.product_service.get_products_by_barcodes(
            barcodes=[item.barcode for item in adding_products_data],
        )
        updating_daily_diet = await self.diet_repository.get_daily_diet_by_id(
            uow=uow,
            daily_diet_id=daily_diet_id,
        )
        merged_product_list = [
            {**product.dict(), **amount.dict()}
            for product, amount in zip(products_full_info, adding_products_data)
        ]
        updated_daily_diet, updated_meal = await self._actualize_daily_diet_fact(
            updating_daily_diet=updating_daily_diet,
            meal_type=meal_type,
            product_list=merged_product_list,
        )
        result = await self.diet_repository.update_daily_diet_meal(
            uow=uow,
            updated_daily_diet=updated_daily_diet,
            meal_type=meal_type,
            updated_meal=updated_meal,
        )
        await self.product_service.save_product_to_history(uow, merged_product_list)
        await uow.commit()
        return result

    async def create_diet_templates(self, uow: AsyncSession, training_plan_id: UUID, diets: list[DietIn]) -> int:
        for diet in diets:
            diet.calories = await self.calories_calculator_service.calculate_calories(
                proteins=diet.proteins,
                fats=diet.fats,
                carbs=diet.carbs,
            )

        diet_ids = await self.diet_repository.insert_diet_templates(
            uow=uow,
            training_plan_id=training_plan_id,
            diets=diets,
        )
        await uow.commit()
        return len(diet_ids)

    async def get_daily_customer_diet(
        self, uow: AsyncSession, customer_id: UUID, specific_day: date,
    ) -> DailyDietDtoSchema | None:
        logger.info(f"getting.customer.diet, details=customer_id: {customer_id}, specific_day: {date}")

        diet = await self.diet_repository.get_daily_diet_by_training_plan_date_range(
            uow=uow,
            customer_id=customer_id,
            specific_day=specific_day,
        )

        if diet.diet_day_id is None:
            logger.info(f"creating.customer.daily.diet, details=customer_id: {customer_id}, specific_day: {date}")
            diet = await self.diet_repository.create_daily_diet(
                uow=uow,
                template_diet_id=diet.template_diet_id,
                specific_day=specific_day,
            )
            await uow.commit()

        return diet

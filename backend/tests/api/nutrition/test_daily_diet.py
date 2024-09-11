from datetime import timedelta

import pytest
from unittest.mock import patch

from src.schemas.product_dto import ProductDtoSchema
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_get_customer_daily_diet(create_diets):
    customer_username = create_diets[0].training_plans.customer.username
    specific_day = create_diets[0].training_plans.start_date + timedelta(days=2)

    response = await make_test_http_request(
        url=f"api/nutrition/diets/{specific_day}",
        method="get",
        username=customer_username,
    )

    assert response.status_code == 200

    response = response.json()
    assert "date" in response
    assert "actual_nutrition" in response

    meals = response["actual_nutrition"]
    assert "daily_total" in meals
    assert "breakfast" in meals
    assert "lunch" in meals
    assert "dinner" in meals
    assert "snacks" in meals


@pytest.mark.asyncio
@patch("src.repository.product_repository.ProductRepository.get_products_by_barcodes")
async def test_add_product_to_diet(mock_insert_product, create_diets):
    daily_diet_id = str(create_diets[1].diet_days[0].id)
    customer_username = create_diets[0].training_plans.customer.username

    product_data = {
        "daily_diet_id": daily_diet_id,
        "meal_type": "breakfast",
        "product_data": [
            {"barcode": "123456789", "amount": 300},
            {"barcode": "987654321", "amount": 100},
        ],
    }

    full_product_info_1 = ProductDtoSchema(
        name="Молоко",
        barcode="123456789",
        type="milliliter",
        proteins=20,
        fats=10,
        carbs=20,
        calories=250,
        vendor_name="Простаквашино",
        user_id=str(create_diets[0].training_plans.customer.id),
    )
    full_product_info_2 = ProductDtoSchema(
        name="Геркулес",
        barcode="987654321",
        type="gram",
        proteins=5,
        fats=4,
        carbs=70,
        calories=330,
        vendor_name="Простаквашино",
        user_id=str(create_diets[0].training_plans.customer.id),
    )
    mock_insert_product.return_value = [full_product_info_1, full_product_info_2]

    response = await make_test_http_request(
        url=f"api/nutrition/diets",
        method="post",
        json=product_data,
        username=customer_username,
    )

    assert response.status_code == 201

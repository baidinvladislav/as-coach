import pytest
from unittest.mock import patch

from src.schemas.product_dto import ProductDtoSchema
from src.service.calories_calculator_service import CaloriesCalculatorService
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
@patch("src.repository.product_repository.ProductRepository.get_product_by_barcode")
async def test_get_product(mock_get_product_by_barcode, create_customer):
    mock_product_dto = ProductDtoSchema(
        name="Test Product",
        barcode="123456789",
        type="food",
        proteins=10.0,
        fats=5.0,
        carbs=20.0,
        calories=200,
        vendor_name="Test Vendor",
        user_id=str(create_customer.id),
    )

    mock_get_product_by_barcode.return_value = mock_product_dto

    response = await make_test_http_request(
            url=f"api/nutrition/products/{mock_product_dto.barcode}",
            method="get",
            username=create_customer.username,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
@patch("src.repository.product_repository.ProductRepository.insert_product")
@patch("src.repository.product_repository.ProductRepository.get_product_by_barcode")
async def test_create_product(mock_get_product_by_barcode, mock_insert_product, create_customer):
    product_data = {
        "name": "Творог 5%",
        "barcode": 123456789,
        "type": "gram",
        "proteins": 20,
        "fats": 5,
        "carbs": 0,
        "vendor_name": "Простаквашино",
    }

    calories_calculator = CaloriesCalculatorService()
    calories = await calories_calculator.calculate_calories(
        proteins=product_data["proteins"], fats=product_data["fats"], carbs=product_data["carbs"],
    )

    mock_get_product_by_barcode.return_value = None
    mock_product_dto = ProductDtoSchema(
        name=product_data["name"],
        barcode=product_data["barcode"],
        type=product_data["type"],
        proteins=product_data["proteins"],
        fats=product_data["fats"],
        carbs=product_data["carbs"],
        calories=calories,
        vendor_name=product_data["vendor_name"],
        user_id=str(create_customer.id),
    )
    mock_insert_product.return_value = mock_product_dto

    response = await make_test_http_request(
        url="api/nutrition/products",
        method="post",
        username=create_customer.username,
        json=product_data,
    )

    assert response.status_code == 201

    response_json = response.json()
    assert response_json.get("barcode") is not None
    assert response_json.get("name") is not None


@pytest.mark.asyncio
@patch("src.repository.product_repository.ProductRepository.lookup_products")
async def test_search_product(mock_lookup_products, create_customer):
    mock_product_list_dto = [
            ProductDtoSchema(
            name="Яйца",
            barcode="123456789",
            type="food",
            proteins=12.6,
            fats=10.6,
            carbs=0.6,
            calories=155,
            vendor_name="Окское",
            user_id=str(create_customer.id),
        ),
        ProductDtoSchema(
            name="Яйца",
            barcode="123456789",
            type="food",
            proteins=11.6,
            fats=11.6,
            carbs=0.9,
            calories=154.4,
            vendor_name="Троекурово",
            user_id=str(create_customer.id),
        ),
    ]

    mock_lookup_products.return_value = mock_product_list_dto

    query_text = "Яйца"
    response = await make_test_http_request(
        url=f"api/nutrition/products/lookup/{query_text}",
        method="get",
        username=create_customer.username,
    )

    assert response.status_code == 200
    response_json = response.json()

    for product in response_json:
        assert query_text in product["name"] or query_text in product["vendor_name"]

    fields = ("barcode", "name", "proteins", "fats", "carbs", "calories", "vendor_name")
    for item in response_json:
        for field in fields:
            assert field in item

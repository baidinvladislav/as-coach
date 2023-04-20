import pytest
from httpx import AsyncClient

from src.main import app
from backend.tests.conftest import TEST_CLIENT_PASSWORD


@pytest.mark.anyio
async def test_customer_login_successfully(create_customer):
    """
    Tests success customer login
    """
    login_data = {
        "username": create_customer.username,
        "password": TEST_CLIENT_PASSWORD
    }

    async with AsyncClient(app=app, base_url="http://as-coach") as ac:
        response = await ac.post(
            "/api/login",
            data=login_data,
            headers={"content-type": "application/x-www-form-urlencoded"}
        )

    assert response.status_code == 200

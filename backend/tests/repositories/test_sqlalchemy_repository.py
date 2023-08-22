"""
Tests SQLAlchemy repository
"""

import pytest

from src.core.repositories.sqlalchemy import SQLAlchemyRepository
from src.coach.models import Coach
from src.gym.models import Exercise
from src.customer.utils import generate_random_password


@pytest.mark.asyncio
async def test_create_method_positive(override_get_db):
    """
    Tests method to create new record through SQLAlchemy repo
    """

    repo = SQLAlchemyRepository(model=Coach, session=override_get_db)

    coach_data = {
        "username": "+79253332211",
        "password": generate_random_password(8),
        "first_name": "Станислав"
    }

    coach = await repo.create(**coach_data)

    assert isinstance(coach, Coach)

    assert coach.id is not None
    assert coach.password is not None
    assert coach.username == coach_data["username"]
    assert coach.first_name == coach_data["first_name"]


@pytest.mark.asyncio
async def test_create_method_raise_attribute_error(override_get_db):
    """
    Tests raising error because of invalid attributes
    """

    repo = SQLAlchemyRepository(model=Coach, session=override_get_db)

    coach_data = {
        "username": "+79253332211",
        "password": generate_random_password(8),
        "first_name": "Станислав",
        "fake_field": "some_value"
    }
    with pytest.raises(AttributeError):
        await repo.create(**coach_data)


@pytest.mark.asyncio
async def test_get_method(create_customer, override_get_db):
    """
    Tests the successful receiving of the object
    """

    repo = SQLAlchemyRepository(model=Coach, session=override_get_db)

    customer = create_customer
    result = await repo.get(pk=str(customer.coach.id))

    assert isinstance(result, Coach)


@pytest.mark.asyncio
async def test_get_all_method(override_get_db):
    """
    Tests the successful receiving all objects from table
    """

    repo = SQLAlchemyRepository(model=Exercise, session=override_get_db)

    result = await repo.get_all()

    assert all(list(map(lambda x: isinstance(x, Exercise), result)))


@pytest.mark.asyncio
async def test_filter_method(create_customer, override_get_db):
    """
    Tests the filtering correctness
    """

    repo = SQLAlchemyRepository(model=Exercise, session=override_get_db)

    result = await repo.filter("name", "Жим штанги лежа")

    for exercise in result:
        assert exercise.name == "Жим штанги лежа"

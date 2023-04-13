import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.customer.models import Customer
from src.auth.utils import get_hashed_password
from src.dependencies import get_db
from src.main import app
from src.auth.models import User

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_USER_USERNAME = os.getenv("TEST_USER_USERNAME")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def create_customer(create_user, override_get_db):
    """
    Creates test customer
    """
    test_user = override_get_db.query(User).filter(
        User.username == create_user.username
    ).first()

    if not test_user.customers:
        test_customer = Customer(
            phone_number='+79991119922',
            first_name='Арнольд',
            last_name='Шварцнеггер'
        )

        override_get_db.add(test_customer)
        override_get_db.commit()
        return test_customer
    else:
        return test_user.customers[0]


@pytest.fixture()
def create_user(override_get_db):
    """
    Creates test user
    """
    test_user = override_get_db.query(User).filter(
        User.username == TEST_USER_USERNAME
    ).first()

    if not test_user:
        test_user = User(
            username=TEST_USER_USERNAME,
            first_name='Владислав',
            password=get_hashed_password(TEST_USER_PASSWORD)
        )

        override_get_db.add(test_user)
        override_get_db.commit()

    return test_user


@pytest.fixture()
def override_get_db():
    """
    Creates session to testing db
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """
    In the beginning on each test creates database schema,
    also changes production db to testing db
    """
    from src.database import Base

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db

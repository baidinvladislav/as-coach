"""
Database settings module
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

from .config import DATABASE_URL, TEST_ENV


if bool(TEST_ENV):
    load_dotenv()
    TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
    engine = create_engine(str(TEST_DATABASE_URL))
else:
    engine = create_engine(str(DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

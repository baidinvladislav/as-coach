from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum

from PIL import Image
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import set_attribute

from src import Coach, Customer
from src.shared.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ALGORITHM, JWT_SECRET_KEY,
    JWT_REFRESH_SECRET_KEY,
    STATIC_DIR,
)
from src.utils import verify_password
from src.presentation.schemas.login import UserLoginData
from src.presentation.schemas.register import UserRegistrationData

USER_MODEL = Coach | Customer


class UserType(Enum):
    COACH = "coach"
    CUSTOMER = "customer"


class UserService(ABC):
    """Contains base user logic"""

    @abstractmethod
    async def register_user(self, uow: AsyncSession, data: UserRegistrationData) -> USER_MODEL:
        raise NotImplementedError

    @abstractmethod
    async def authorize_user(self, uow: AsyncSession, user: USER_MODEL, data: UserLoginData) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_user_profile(self, uow: AsyncSession, user: USER_MODEL, **params) -> None:
        raise NotImplementedError

    @staticmethod
    async def generate_jwt_token(username: str, access: bool = False, refresh: bool = False) -> str:
        if not access and not refresh:
            raise ValueError("Specify what token type you're creating")

        time_delta = timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES) if access else int(REFRESH_TOKEN_EXPIRE_MINUTES)
        )
        expires_delta = datetime.utcnow() + time_delta
        to_encode = {"exp": expires_delta, "sub": username}
        encoded_jwt = jwt.encode(
            to_encode,
            JWT_SECRET_KEY if access else str(JWT_REFRESH_SECRET_KEY),
            str(ALGORITHM)
        )
        return encoded_jwt

    @staticmethod
    async def handle_profile_photo(user: USER_MODEL, photo) -> None:
        if photo is not None:
            saving_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            file_name = f"{user.username}_{saving_time}.jpeg"
            photo_path = f"{STATIC_DIR}/{file_name}"

            width, height = 140, 140
            with Image.open(photo.file) as img:
                img.thumbnail((width, height))
                img.save(photo_path, "PNG")

            set_attribute(user, "photo_path", photo_path)

    @staticmethod
    async def confirm_password(user: USER_MODEL, password: str) -> bool:
        if await verify_password(password, str(user.password)):
            return True
        return False

    @staticmethod
    async def set_fcm_token(user: USER_MODEL, fcm_token: str) -> None:
        user.fcm_token = fcm_token

    async def fcm_token_actualize(self, user: USER_MODEL, fcm_token: str) -> bool:
        if user.fcm_token is None or user.fcm_token != fcm_token:
            await self.set_fcm_token(user, fcm_token)
            return True
        else:
            return False

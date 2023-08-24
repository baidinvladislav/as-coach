"""
Module for auth utils
"""

from datetime import datetime, timedelta

from jose import jwt
from pydantic import ValidationError
from passlib.context import CryptContext

from src.auth.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_REFRESH_SECRET_KEY,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_MINUTES
)
from src.core.services.exceptions import TokenExpired, NotValidCredentials

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
    Hashes password

    Args:
        password: string which will be hashed

    Returns:
        hashed password
    """
    return password_context.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    """
    Checks that string is hashed string

    Args:
        password: row password from client request
        hashed_password: hashed password from database user profile

    Returns:
        True if password matches with hashed_password otherwise False
    """
    is_identified = password_context.identify(hashed_password)
    if not is_identified:
        return False

    is_verified = password_context.verify(password, hashed_password)
    if is_verified:
        return True
    return False


async def create_access_token(subject: str) -> str:
    """
    Creates access token

    Args:
        subject: user's username

    Returns:
        access token
    """
    time_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))  # type: ignore
    expires_delta = datetime.utcnow() + time_delta
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(JWT_SECRET_KEY), str(ALGORITHM))
    return encoded_jwt


async def create_refresh_token(subject: str) -> str:
    """
    Creates refresh token

    Args:
        subject: user's username

    Returns:
        refresh token
    """
    time_delta = timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))  # type: ignore
    expires_delta = datetime.utcnow() + time_delta
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(JWT_REFRESH_SECRET_KEY), str(ALGORITHM))
    return encoded_jwt


async def decode_jwt_token(token: str):
    """
    Decodes given token
    """
    # TODO: fix it
    from src.infrastructure.schemas.auth import TokenPayload

    try:
        payload = jwt.decode(
            token, str(JWT_SECRET_KEY), algorithms=[str(ALGORITHM)]
        )
        token_data = TokenPayload(**payload)

        expiration_time = datetime.fromtimestamp(token_data.exp)
        if expiration_time < datetime.now():
            raise TokenExpired

        return token_data

    except (jwt.JWTError, ValidationError):  # type: ignore
        raise NotValidCredentials


def validate_password(password: str):
    """
    Password can be at least 8 characters
    """
    if 7 < len(password) < 129:
        return password
    raise ValueError("Password must be greater than 7 symbols and less than 129 symbols")

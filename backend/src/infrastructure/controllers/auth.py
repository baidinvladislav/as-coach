"""
Contains routes for auth service.
"""

import shutil
from datetime import date, datetime
from typing import Union, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
    Form
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import set_attribute
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from src.auth.dependencies import get_current_user
from src.coach.dependencies import get_coach_service, get_customer_service
from src.core.services.coach import CoachService, UsernameIsTaken, NotValidPassword
from src.core.services.customer import CustomerService
from src.dependencies import get_db
from src.models import Gender
from src.infrastructure.schemas.auth import (
    UserProfile,
    NewUserPassword,
    LoginResponse,
    CoachRegisterIn,
    CoachRegisterOut
)
from src.customer.models import Customer
from src.coach.models import Coach
from src.auth.utils import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
    password_context
)
from src.config import STATIC_DIR

auth_router = APIRouter()


@auth_router.post(
    "/signup",
    summary="Create new coach",
    status_code=status.HTTP_201_CREATED,
    response_model=CoachRegisterOut)
async def register_user(
        coach_data: CoachRegisterIn,
        service: CoachService = Depends(get_coach_service)
) -> dict:
    """
    Registration endpoint, creates new coach in database

    Args:
        coach_data: data schema for coach registration
        service: service for interacting with Coach domain
    Raises:
        400 in case if user with the phone number already created
    Returns:
        dictionary with just created user,
        id, first_name and username as keys
    """

    try:
        coach = await service.register_coach(coach_data)
    except UsernameIsTaken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )

    return {
        "id": str(coach.id),
        "first_name": coach.first_name,
        "username": coach.username,
        "access_token": await create_access_token(str(coach.username)),
        "refresh_token": await create_refresh_token(str(coach.username))
    }


@auth_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        coach_service: CoachService = Depends(get_coach_service),
        customer_service: CustomerService = Depends(get_customer_service)
) -> dict:
    """
    Login endpoint authenticates user

    Args:
        form_data: data schema for user login
        coach_service: service for interacting with Coach domain
        customer_service: service for interacting with Customer domain
    Raises:
        404 if specified user was not found
        400 in case if user is found but password does not match
    Returns:
        access_token and refresh_token inside dictionary
    """

    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty fields"
        )

    coach = await coach_service.find_by_username(form_data.username)
    customer = await customer_service.find_by_username(form_data.username)

    user_in_db = coach or customer

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Any user is not found"
        )

    try:
        if coach:
            is_auth = await coach_service.authorize(coach, form_data.password)
        else:
            is_auth = await customer_service.authorize(customer, form_data.password)

    except NotValidPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not valid password for user_id: {user_in_db.id}"
        )

    else:
        if is_auth:
            return {
                "id": str(user_in_db.id),
                "user_type": "coach" if coach else "customer",
                "first_name": user_in_db.first_name,
                "access_token": await create_access_token(str(user_in_db.username)),
                "refresh_token": await create_refresh_token(str(user_in_db.username)),
                "password_changed": bool(password_context.identify(user_in_db.password))
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown error during authentication user_id: {user_in_db.id}"
            )


@auth_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get details of currently logged in user")
async def get_me(
        user: Union[Coach, Customer] = Depends(get_current_user)) -> dict:
    """
    Returns short info about current user
    Endpoint can be used by both a coach and a customer

    Args:
        user: coach or customer object from get_current_user dependency

    Returns:
        dict: short info about current user
    """

    return {
        "id": str(user.id),
        "user_type": "coach" if isinstance(user, Coach) else "customer",
        "username": user.username,
        "first_name": user.first_name
    }


@auth_router.get(
    "/profiles",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    summary="Get user profile")
async def get_profile(
        user: Union[Coach, Customer] = Depends(get_current_user)
) -> dict:
    """
    Returns full info about user
    Endpoint can be used by both the coach and the customer

    Args:
        user: coach or customer object from get_current_user dependency

    Returns:
        dict: full info about current user
    """

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": "coach" if isinstance(user, Coach) else "customer",
        "gender": user.gender,
        "birthday": user.birthday,
        "email": user.email,
        "username": user.username,
        "photo_link": user.photo_path.split('/backend')[1] if user.photo_path else None
    }


@auth_router.post(
    "/profiles",
    summary="Update user profile",
    response_model=UserProfile,
    status_code=status.HTTP_200_OK)
async def update_profile(
        first_name: str = Form(...),
        username: str = Form(...),
        last_name: str = Form(None),
        photo: UploadFile = File(None),
        gender: Optional[Gender] = Form(None),
        birthday: date = Form(None),
        email: str = Form(None),
        database: Session = Depends(get_db),
        user: Union[Coach, Customer] = Depends(get_current_user)
) -> dict:
    """
    Updated full info about user
    Endpoint can be used by both the coach and the customer

    Args:
        first_name: client value from body
        username: client value from body
        last_name: client value from body
        photo: client file from body
        gender: client value from body
        birthday: client value from body
        email: client value from body
        database: dependency injection for access to database
        user: coach or customer object from get_current_user dependency

    Returns:
        dictionary with updated full user info
    """

    if photo is not None:
        saving_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name = f"{user.username}_{saving_time}.jpeg"
        photo_path = f"{STATIC_DIR}/{file_name}"
        with open(photo_path, 'wb') as buffer:
            shutil.copyfileobj(photo.file, buffer)

        set_attribute(user, "photo_path", photo_path)

    set_attribute(user, "modified", datetime.now())

    if isinstance(user, Coach):
        user_class = Coach
    else:
        user_class = Customer

    query = (
        update(user_class)
        .where(user_class.id == str(user.id))
        .values(
            first_name=first_name,
            username=username,
            last_name=last_name,
            gender=gender,
            birthday=birthday,
            email=email
        )
    )

    await database.execute(query)
    await database.commit()
    await database.refresh(user)

    if user.photo_path:
        photo_link = user.photo_path.split('/backend')[1]
    else:
        photo_link = None

    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "user_type": "coach" if isinstance(user, Coach) else "customer",
        "gender": user.gender,
        "birthday": user.birthday,
        "email": user.email,
        "username": user.username,
        "photo_link": photo_link
    }


@auth_router.post(
    "/confirm_password",
    summary="Confirm current user password",
    status_code=status.HTTP_200_OK)
async def confirm_password(
        current_password: str = Form(...),
        user: Union[Coach, Customer] = Depends(get_current_user)
) -> dict:
    """
    Confirms that user knows current password before it is changed.

    Args:
        current_password: current user password
        user: user object from get_current_user dependency

    Returns:
        success or failed response
    """

    if verify_password(current_password, str(user.password)):
        return {"confirmed_password": True}

    return {"confirmed_password": False}


@auth_router.patch(
    "/change_password",
    summary="Change user password",
    status_code=status.HTTP_200_OK)
async def change_password(
        new_password: NewUserPassword,
        database: Session = Depends(get_db),
        user: Union[Coach, Customer] = Depends(get_current_user)
) -> dict:
    """
    Changes user password.
    Validation set in schemas.

    Args:
        new_password: new user password
        database: dependency injection for access to database
        user: user object from get_current_user dependency

    Returns:
        success response
    """

    ex_password = user.password
    set_attribute(user, "password", get_hashed_password(new_password.password))
    database.commit()
    return {"changed_password": True if user.password != ex_password else False}

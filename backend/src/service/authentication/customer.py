"""
Service for Customer role functionality
"""

from typing import Optional, Type
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm

from src import Customer
from src.utils import verify_password
from src.repository.abstract import AbstractRepository
from src.service.authentication.exceptions import NotValidCredentials
from src.service.authentication.profile import ProfileService, ProfileType
from src.service.telegram.adapter import TelegramAdapter


class CustomerService(ProfileService):
    """
    Implements logic to interact with Customer domain

    Attributes:
        user: Customer: customer ORM instance
        user_type: str: mark as customer role
        customer_repository: repository to interacting with storage using customer domain
    """

    def __init__(self, customer_repository: AbstractRepository, adapter: Type['TelegramAdapter']):
        self.user = None
        self.user_type = ProfileType.CUSTOMER.value
        self.customer_repository = customer_repository
        self.telegram_adapter = adapter

    async def get_customers_by_coach_id(self, coach_id: str):
        customers_aggregates = await self.customer_repository.provide_customers_by_coach_id(coach_id)

        customers = []
        archive_customers = []
        for customer in customers_aggregates:
            last_plan_end_date = customer[4]

            if last_plan_end_date and datetime.now().date() - last_plan_end_date > timedelta(days=30):
                archive_customers.append({
                    "id": str(customer[0]),
                    "first_name": customer[1],
                    "last_name": customer[2],
                    "phone_number": customer[3],
                    "last_plan_end_date": last_plan_end_date.strftime("%Y-%m-%d")
                })
            else:
                customers.append({
                    "id": str(customer[0]),
                    "first_name": customer[1],
                    "last_name": customer[2],
                    "phone_number": customer[3],
                    "last_plan_end_date": last_plan_end_date.strftime("%Y-%m-%d") if last_plan_end_date else None
                })

        customers.extend(archive_customers)
        return customers

    async def register(self, **kwargs) -> Customer:
        """
        Temperately customer registration implemented by Coach's invites
        """
        ...

    async def authorize(self, form_data: OAuth2PasswordRequestForm, fcm_token: str) -> Customer:
        """
        Customer logs in with default password in the first time after receive invite.
        After customer changes password it logs in with own hashed password.

        Args:
            form_data: customer credentials passed by client
            fcm_token: token to send push notification on user device

        Raises:
            NotValidCredentials: in case if credentials aren't valid
        """
        password_in_db = str(self.user.password)
        if password_in_db == form_data.password \
                or await verify_password(form_data.password, password_in_db):

            if self.user.fcm_token != fcm_token:
                await self.set_fcm_token(fcm_token)
                await self.customer_repository.update(str(self.user.id), fcm_token=fcm_token)

            return self.user

        raise NotValidCredentials

    async def find(self, filters: dict) -> Optional[Customer]:
        """
        Provides customer from database in case it is found.
        Save customer instance to user attr.

        Args:
            filters: attributes and these values
        """
        foreign_keys, sub_queries = ["training_plans"], ["trainings", "diets"]
        customer = await self.customer_repository.filter(
            filters=filters,
            foreign_keys=foreign_keys,
            sub_queries=sub_queries
        )

        if customer:
            self.user = customer[0]
            return self.user

    # TODO: return numbers of updated rows
    async def update(self, **params) -> None:
        """
        Updates customer data in database

        Args:
            params: parameters for customer updating
        """
        if "photo" in params:
            await self.handle_profile_photo(params.pop("photo"))
        await self.customer_repository.update(str(self.user.id), **params)

    async def _send_invite(self, username: str, message: str) -> None:
        """
        Invites customer to application providing One Time Password to first log in

        Args:
            username: customer's username
            message: text with invitation and OTP
        """
        async with self.telegram_adapter() as tlg_session:
            await tlg_session.send_message_to_user(
                username=username,
                message=message,
            )

    async def create(self, coach_id: str, **kwargs) -> Customer:
        """
        Creates new customer in database

        Args:
            coach_id: customer's coach
            kwargs: any required params for customer creating

        Returns:
            customer: Customer instance
        """
        self.user = await self.customer_repository.create(coach_id=coach_id, **kwargs)
        await self._send_invite(self.user.username, f"Your OTP is {self.user.password}")
        await self.update(invited_at=datetime.now())
        return self.user

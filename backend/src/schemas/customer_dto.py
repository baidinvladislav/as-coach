from datetime import date
from uuid import UUID

from pydantic import BaseModel, validator

from src import Gender


class CustomerDtoSchema(BaseModel):
    id: UUID
    username: str | None
    first_name: str
    coach_id: UUID
    fcm_token: str | None
    last_name: str | None
    password: str
    telegram_username: str | None
    gender: str | None | Gender
    birthday: date | None
    email: str | None
    photo_link: str | None

    class Config:
        orm_mode = True

    @classmethod
    @validator("gender", pre=True, always=True)
    def lowercase_gender(cls, gender_enum: Gender | None) -> str | None:
        if gender_enum is not None:
            return gender_enum.value.lower()
        return None


class CustomerShortDtoSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str | None
    username: str | None
    last_plan_end_date: date | None

    class Config:
        orm_mode = True

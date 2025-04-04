import datetime
import enum
import uuid

from sqlalchemy import (
    Column, DateTime, String, Enum, Date, ForeignKey, Text, Integer, JSON, Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import RelationshipProperty, relationship

from src import Base


class BaseModel:
    """
    Base model class with common column.
    """
    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created = Column("created", DateTime, default=datetime.datetime.now, nullable=False)
    modified = Column("modified", DateTime)
    deleted = Column("deleted", DateTime)


class Gender(enum.Enum):
    """
    Enum for selecting customer gender.
    """
    MALE = "male"
    FEMALE = "female"


class Coach(Base, BaseModel):
    """
    Application user model.
    """
    __tablename__ = "coach"
    __table_args__ = {"extend_existing": True}

    username = Column("username", String(100), nullable=False, index=True, doc="It's phone number")
    password = Column("password", String(255), nullable=False)
    first_name = Column("first_name", String(50), nullable=True)
    last_name = Column("last_name", String(50), nullable=True)
    gender: Column = Column("gender", Enum(Gender), nullable=True)
    customers: RelationshipProperty = relationship(
        "Customer",
        cascade="all,delete-orphan",
        back_populates="coach"
    )
    email = Column("email", String(100), nullable=True)
    birthday = Column("birthday", Date, nullable=True)
    photo_path = Column("photo_path", String(255), nullable=True)
    exercises: RelationshipProperty = relationship(
        "Exercise",
        cascade="all,delete-orphan",
        back_populates="coach"
    )
    fcm_token = Column("fcm_token", String(255), nullable=False)

    def __repr__(self):
        return f"Coach: {self.username}"


class Customer(Base, BaseModel):
    """
    Customer, created by coach, gets training plan.
    """
    __tablename__ = "customer"
    __table_args__ = {'extend_existing': True}

    username = Column("username", String(100), nullable=True, index=True, doc="It's phone number")
    telegram_username = Column("telegram_username", String(50), nullable=True, index=True, doc="It's telegram username")
    password = Column("password", String(255), nullable=True)
    first_name = Column("first_name", String(50), nullable=False)
    last_name = Column("last_name", String(50), nullable=False)
    gender: Column = Column("gender", Enum(Gender), nullable=True)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coach.id", ondelete="CASCADE"))
    coach: RelationshipProperty = relationship("Coach", back_populates="customers")
    training_plans: RelationshipProperty = relationship(
        "TrainingPlan",
        cascade="all,delete-orphan",
        back_populates="customer"
    )
    history_products: RelationshipProperty = relationship(
        "CustomerHistoryProducts",
        cascade="all,delete-orphan",
        back_populates="customer"
    )
    birthday = Column("birthday", Date, nullable=True)
    photo_path = Column("photo_path", String(255), nullable=True)
    email = Column("email", String(100), nullable=True)
    fcm_token = Column("fcm_token", String(255), nullable=True)

    def __repr__(self):
        return f"Customer: {self.last_name} {self.first_name}"


class CustomerHistoryProducts(Base, BaseModel):
    """
    Customer consumed products history.
    """
    __tablename__ = "product_history"
    __table_args__ = {'extend_existing': True}

    name = Column("name", String(255), nullable=False)
    type = Column("type", String(50), nullable=False)   # TODO: make enum
    proteins = Column("proteins", Float, nullable=False)
    fats = Column("fats", Float, nullable=False)
    carbs = Column("carbs", Float, nullable=False)
    calories = Column("calories", Float, nullable=False)
    vendor_name = Column("vendor_name", String(255), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id", ondelete="CASCADE"), nullable=False)
    customer: RelationshipProperty = relationship("Customer", back_populates="history_products")
    barcode = Column("barcode", String(50), nullable=False)
    amount = Column("amount", Float, nullable=False)

    def __repr__(self):
        return f"Product history: {self.customer_id} {self.product_barcode} {self.product_amount}"


class TrainingPlan(Base, BaseModel):
    """
    Contains training, diets, notes and also relates to customer.
    """
    __tablename__ = "trainingplan"

    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    diets: RelationshipProperty = relationship("Diet", back_populates="training_plans")
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.id", ondelete="CASCADE"))
    customer: RelationshipProperty = relationship("Customer", back_populates="training_plans")
    trainings: RelationshipProperty = relationship(
        "Training",
        cascade="all,delete-orphan",
        back_populates="training_plan"
    )
    notes = Column("notes", Text, nullable=True)
    set_rest = Column("set_rest", Integer, default=60)
    exercise_rest = Column("exercise_rest", Integer, default=120)

    def __repr__(self):
        return f"Training_plan:  from {self.start_date} to {self.end_date}"


class Diet(Base, BaseModel):
    """
    Contains nutrients amount within the training plan domain.
    The recommended diet by the coach is a subdomain of the training plan domain.
    """
    __tablename__ = "diet"

    total_proteins = Column("total_proteins", Integer, nullable=False)
    total_fats = Column("total_fats", Integer, nullable=False)
    total_carbs = Column("total_carbs", Integer, nullable=False)
    total_calories = Column("total_calories", Integer, nullable=False)
    training_plan_id = Column(UUID(as_uuid=True), ForeignKey("trainingplan.id", ondelete="CASCADE"))
    # TODO: сейчас у нас один уже план, нужно поменять атрибут на training_plan
    training_plans: RelationshipProperty = relationship("TrainingPlan", back_populates="diets")
    diet_days = relationship("DietDays", back_populates="diet", cascade="all, delete-orphan")

    def __repr__(self):
        return f"diet: {self.total_proteins}/{self.total_fats}/{self.total_carbs}/{self.total_calories}"


class DietDays(Base, BaseModel):
    __tablename__ = "dietday"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    date = Column(Date, nullable=False)

    breakfast = Column(JSON, default={})
    lunch = Column(JSON, default={})
    dinner = Column(JSON, default={})
    snacks = Column(JSON, default={})

    diet_id = Column(UUID(as_uuid=True), ForeignKey("diet.id"), nullable=False)
    diet = relationship("Diet", back_populates="diet_days")

    def __repr__(self):
        return f"Diet day: {self.date}"


class Training(Base, BaseModel):
    """
    Contains training's exercises.
    """
    __tablename__ = "training"

    name = Column("name", String(50), nullable=False)
    training_plan_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trainingplan.id", ondelete="CASCADE"),
        nullable=False
    )
    training_plan: RelationshipProperty = relationship(
        "TrainingPlan",
        back_populates="trainings"
    )
    exercises: RelationshipProperty = relationship(
        "Exercise",
        secondary="exercisesontraining",
        back_populates="trainings"
    )

    def __repr__(self):
        return f"training: {self.name}"


class MuscleGroup(Base, BaseModel):
    """
    Muscle group for exercises
    """
    __tablename__ = "musclegroup"

    name = Column("name", String(50), nullable=False)
    exercises: RelationshipProperty = relationship(
        "Exercise",
        back_populates="muscle_group",
        cascade="all,delete-orphan"
    )


class Exercise(Base, BaseModel):
    """
    Represents exercises in training.
    User can create custom exercises
    but user can not see custom exercises other users.
    """
    __tablename__ = "exercise"

    name = Column("name", String(50), nullable=False)
    coach_id = Column(UUID(as_uuid=True), ForeignKey("coach.id", ondelete="CASCADE"))
    coach: RelationshipProperty = relationship("Coach", back_populates="exercises")
    muscle_group_id = Column(UUID(as_uuid=True), ForeignKey("musclegroup.id"), nullable=False)
    muscle_group: RelationshipProperty = relationship("MuscleGroup", back_populates="exercises")
    trainings: RelationshipProperty = relationship(
        "Training",
        secondary="exercisesontraining",
        back_populates="exercises"
    )

    def __repr__(self):
        return f"Exercise: {self.name}"


class ExercisesOnTraining(Base, BaseModel):
    """
    Model for M2M relationship Training and Exercise.
    """
    __tablename__ = "exercisesontraining"

    training_id = Column(UUID(as_uuid=True), ForeignKey("training.id", ondelete="CASCADE"))
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercise.id", ondelete="CASCADE"))
    sets = Column("sets", JSON, default=[])
    superset_id = Column(UUID(as_uuid=True), nullable=True)
    ordering = Column("ordering", Integer, default=0)

    def __repr__(self):
        return f"Exercise on training: {self.id}"

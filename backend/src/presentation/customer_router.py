import logging
from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.service.coach_service import CoachService
from src.service.customer_service import CustomerService
from src.service.training_plan_service import TrainingPlanService, TrainingPlanCreationException
from src.presentation.schemas.customer_schema import (
    CustomerOut,
    CustomerCreateIn,
)
from src.presentation.schemas.training_plan_schema import TrainingPlanIn, TrainingPlanOut, TrainingPlanOutFull
from src.presentation.schemas.register_schema import CustomerRegistrationData
from src.shared.dependencies import (
    provide_database_unit_of_work,
    provide_customer_service,
    provide_user_service,
    provide_training_plan_service,
    provide_push_notification_service,
)
from src.utils import validate_uuid, generate_random_password
from src.service.notification_service import NotificationService
from src.shared.config import OTP_LENGTH

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

customer_router = APIRouter()


@customer_router.post(
    "/customers",
    summary="Create new customer",
    status_code=status.HTTP_201_CREATED,
    response_model=CustomerOut)
async def create_customer(
    customer_data: CustomerCreateIn,
    user_service: CoachService = Depends(provide_user_service),
    customer_service: CustomerService = Depends(provide_customer_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> CustomerOut:
    """
    Creates new customer for coach

    Args:
        customer_data: data to create new customer
        user_service: service for interacting with profile
        customer_service: service for interacting with customer
        uow: db session injection
    Raises:
        400 in case if customer with the phone number already created
        400 in case if couple last name and first name already exist
    Returns:
        dictionary with just created customer
        id, first_name, last_name and phone_number are keys
    """
    user = user_service.user

    customer_in_db = await customer_service.get_customer_by_username(
        uow=uow, username=customer_data.phone_number
    )
    if customer_data.phone_number and customer_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer {customer_in_db.first_name} {customer_in_db.last_name} "
                   f"with this phone number already exists."
        )

    customer_in_db = await customer_service.get_customer_by_full_name_for_coach(
        uow=uow,
        coach_id=str(user.id),
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
    )
    if customer_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer full name: {customer_data.first_name} "
                   f"{customer_data.last_name} already exists."
        )

    customer_reg_data = CustomerRegistrationData(
        coach_id=str(user.id),
        coach_name=user.first_name,
        telegram_username=customer_data.phone_number,
        password=generate_random_password(OTP_LENGTH),
        first_name=customer_data.first_name,
        last_name=customer_data.last_name,
    )

    customer = await customer_service.register(uow, data=customer_reg_data)

    return CustomerOut(
        id=str(customer.id),
        first_name=customer.first_name,
        last_name=customer.last_name,
        phone_number=customer.username,
        last_plan_end_date=None,
    )


@customer_router.get(
    "/customers",
    summary="Gets all user's customers",
    status_code=status.HTTP_200_OK)
async def get_customers(
    coach_service: CoachService = Depends(provide_user_service),
    customer_service: CustomerService = Depends(provide_customer_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> List[dict[str, Any]]:
    """
    Gets all customer for current coach

    Args:
        coach_service: current application coach
        customer_service: service to work with customer domain
        uow: db session injection
    Returns:
        list of customers
    """
    coach = coach_service.user
    customers = await customer_service.get_customers_by_coach_id(uow, str(coach.id))
    return customers


@customer_router.get(
    "/customers/{customer_id}",
    response_model=CustomerOut,
    status_code=status.HTTP_200_OK)
async def get_customer(
    customer_id: str,
    user_service: CoachService = Depends(provide_user_service),
    customer_service: CustomerService = Depends(provide_customer_service),
    training_plan_service: TrainingPlanService = Depends(provide_training_plan_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> CustomerOut:
    """
    Gets specific customer by ID.

    Args:
        customer_id: str(UUID) of specified customer.
        user_service: service for interacting with profile
        customer_service: service for interacting with customer
        training_plan_service: service for interacting with customer training plans
        uow: db session injection

    Raise:
        HTTPException: 400 when passed is not correct UUID as customer_id.
        HTTPException: 404 when customer not found.
        HTTPException: 400 when specified customer does not belong to the current coach.
    """
    if not await validate_uuid(customer_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passed customer_id is not correct UUID value"
        )

    customer = await customer_service.get_customer_by_pk(uow, pk=customer_id)

    if str(customer.coach_id) != str(user_service.user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The client belong to another coach"
        )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} not found"
        )

    training_plans = await training_plan_service.get_customer_training_plans(uow, str(customer.id))
    return CustomerOut(
        id=str(customer.id),
        first_name=customer.first_name,
        last_name=customer.last_name,
        phone_number=customer.username,
        last_plan_end_date=training_plans[0].end_date.strftime("%Y-%m-%d") if training_plans else None
    )


@customer_router.post(
    "/customers/{customer_id}/training_plans",
    summary="Create new training plan for customer",
    status_code=status.HTTP_201_CREATED,
    response_model=TrainingPlanOut)
async def create_training_plan(
    training_plan_data: TrainingPlanIn,
    customer_id: str,
    customer_service: CustomerService = Depends(provide_customer_service),
    user_service: CoachService = Depends(provide_user_service),
    training_plan_service: TrainingPlanService = Depends(provide_training_plan_service),
    push_notification_service: NotificationService = Depends(provide_push_notification_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> TrainingPlanOut:
    """
    Creates new training plan for specified customer.
    Notifies customer that he got new training plan.

    Args:
        training_plan_data: data from application user to create new training plan
        customer_id: customer's str(UUID)
        customer_service: service for interacting with customer
        user_service: service for interacting with profile
        training_plan_service: service for interacting with customer training plans
        push_notification_service: service responsible to send push notification through FireBase service
        uow: db session injection
    """
    customer = await customer_service.get_customer_by_pk(uow, pk=customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with id {customer_id} not found")

    try:
        training_plan = await training_plan_service.create_training_plan(
            uow=uow,
            customer_id=customer_id,
            data=training_plan_data,
        )
    except TrainingPlanCreationException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unknown error during training plan creation",
        )

    push_tittle = "Создан новый тренировочный план"
    push_body = f"с {training_plan.start_date} до {training_plan.end_date}"
    notification_data = {"title": push_tittle, "body": push_body}
    await push_notification_service.send_push_notification(customer.fcm_token, notification_data)

    return TrainingPlanOut(
        id=str(training_plan.id),
        start_date=training_plan.start_date.strftime("%Y-%m-%d"),
        end_date=training_plan.end_date.strftime("%Y-%m-%d"),
        number_of_trainings=len(training_plan.trainings),
        proteins="/".join([str(diet.total_proteins) for diet in training_plan.diets]),
        fats="/".join([str(diet.total_fats) for diet in training_plan.diets]),
        carbs="/".join([str(diet.total_carbs) for diet in training_plan.diets]),
        calories="/".join([str(diet.total_calories) for diet in training_plan.diets]),
    )


@customer_router.get(
    "/customers/{customer_id}/training_plans",
    summary="Returns all training plans for customer",
    status_code=status.HTTP_200_OK)
async def get_all_training_plans(
    customer_id: str,
    user_service: CoachService = Depends(provide_user_service),
    customer_service: CustomerService = Depends(provide_customer_service),
    training_plan_service: TrainingPlanService = Depends(provide_training_plan_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> list[TrainingPlanOut]:
    """
    Returns all training plans for specific customer
    Endpoint can be used by both the coach and the customer

    Args:
        customer_id: customer's str(UUID)
        user_service: service for interacting with profile
        customer_service: service for interacting with customer
        training_plan_service: service responsible for training plans creation
        uow: db session injection
    """
    customer = await customer_service.get_customer_by_pk(uow, pk=customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"customer with id={customer_id} doesn't exist")

    training_plans = await training_plan_service.get_customer_training_plans(uow, str(customer.id))

    response = [
        TrainingPlanOut(
            id=str(training_plan.id),
            start_date=training_plan.start_date.strftime("%Y-%m-%d"),
            end_date=training_plan.end_date.strftime("%Y-%m-%d"),
            number_of_trainings=training_plan.number_of_trainings,
            proteins="/".join([str(diet.total_proteins) for diet in training_plan.diets]),
            fats="/".join([str(diet.total_fats) for diet in training_plan.diets]),
            carbs="/".join([str(diet.total_carbs) for diet in training_plan.diets]),
            calories="/".join([str(diet.total_calories) for diet in training_plan.diets]),
        )
        for training_plan in training_plans
    ]

    return response


@customer_router.get(
    "/customers/{customer_id}/training_plans/{training_plan_id}",
    response_model=TrainingPlanOutFull,
    status_code=status.HTTP_200_OK)
async def get_training_plan(
    training_plan_id: UUID,
    customer_id: str,  # TODO: make uuid it raises 500 now if not uuid
    user_service: CoachService = Depends(provide_user_service),
    training_plan_service: TrainingPlanService = Depends(provide_training_plan_service),
    customer_service: CustomerService = Depends(provide_customer_service),
    uow: AsyncSession = Depends(provide_database_unit_of_work),
) -> TrainingPlanOutFull:
    """
    Gets full info for specific training plan by their ID
    Endpoint can be used by both the coach and the customer

    Args:
        training_plan_id: str(UUID) of specified training plan
        customer_id: str(UUID) of specified customer
        user_service: service for interacting with profile
        training_plan_service: service for interacting with customer training plans
        customer_service: service for interacting with customer
        uow: db session injection

    Raise:
        HTTPException: 404 when customer or training plan are not found
    """
    customer = await customer_service.get_customer_by_pk(uow, pk=customer_id)
    if customer is None:
        logger.info(f"customer.does.not.exist, id={customer_id}")
        raise HTTPException(status_code=404, detail=f"Customer with id={customer_id} doesn't exist")

    training_plan = await training_plan_service.get_training_plan_by_id(uow, training_plan_id)
    if training_plan is None:
        logger.info(f"training.plan.does.not.exist, id={training_plan_id}")
        raise HTTPException(status_code=404, detail=f"Training plan with id={training_plan_id} doesn't exist")

    response = TrainingPlanOutFull(
        id=training_plan.id,
        start_date=training_plan.start_date,
        end_date=training_plan.end_date,
        proteins=training_plan.proteins,
        fats=training_plan.fats,
        carbs=training_plan.carbs,
        calories=training_plan.calories,
        trainings=training_plan.trainings,
        set_rest=training_plan.set_rest,
        exercise_rest=training_plan.exercise_rest,
        notes=training_plan.notes,
    )

    # TODO: сделать на уровне слоя данных, поняв где нарушается сортировка
    for training in response.trainings:
        training.exercises.sort(key=lambda x: x.ordering)

    return response

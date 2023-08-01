"""
Gym routing
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, or_
from sqlalchemy.orm import Session, selectinload

from src.coach.dependencies import get_current_coach
from src.dependencies import get_db
from src.gym.models import Exercise, MuscleGroup
from src.gym.schemas import ExerciseCreateIn, ExerciseCreateOut
from src.coach.models import Coach

gym_router = APIRouter()


@gym_router.post(
    "/exercises",
    summary="Create new exercise",
    status_code=status.HTTP_201_CREATED,
    response_model=ExerciseCreateOut)
async def create_exercise(
        exercise_data: ExerciseCreateIn,
        database: Session = Depends(get_db),
        current_user: Coach = Depends(get_current_coach)) -> dict:
    """
    Creates new exercise for coach

    Args:
        exercise_data: data to create new exercise
        database: dependency injection for access to database
        current_user: returns current application user

    Returns:
        dictionary with just created exercise id, name, muscle_group's name as keys
    """
    exercise = Exercise(
        name=exercise_data.name,
        muscle_group_id=exercise_data.muscle_group_id,
        coach_id=str(current_user.id)
    )

    database.add(exercise)
    database.commit()

    return {
        "id": str(exercise.id),
        "muscle_group": exercise.muscle_group.name,
        "name": exercise.name
    }


@gym_router.get(
    "/exercises",
    summary="Returns all exercises",
    status_code=status.HTTP_200_OK)
async def get_exercises(
        database: Session = Depends(get_db),
        current_user: Coach = Depends(get_current_coach)) -> list:
    """
    Returns all exercises for coach

    Args:
        database: dependency injection for access to database
        current_user: returns current application user

    Returns:
        list of exercises
    """
    exercises = await database.execute(
        select(Exercise).where(
            or_(
                Exercise.coach_id.is_(None),
                Exercise.coach_id == str(current_user.id)
            )
        ).options(
            selectinload(Exercise.muscle_group)
        )
    )

    response = []
    for exercise in exercises.scalars():
        response.append({
            "id": str(exercise.id),
            "name": exercise.name,
            "muscle_group": exercise.muscle_group.name,
            "muscle_group_id": str(exercise.muscle_group.id)
        })

    return response


@gym_router.get(
    "/muscle_groups",
    summary="Returns all muscle groups",
    status_code=status.HTTP_200_OK)
async def get_muscle_groups(
        database: Session = Depends(get_db),
        current_user: Session = Depends(get_current_coach)) -> list:
    """
    Returns all muscle groups for coach

    Args:
        database: dependency injection for access to database
        current_user: returns current application user

    Returns:
        list of muscle groups
    """
    muscle_groups = database.query(MuscleGroup).all()

    response = []
    for muscle_group in muscle_groups:
        response.append({
            "id": str(muscle_group.id),
            "name": muscle_group.name
        })

    return response

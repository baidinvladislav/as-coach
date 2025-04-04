from datetime import date, timedelta
import pytest

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from src import TrainingPlan, MuscleGroup, ExercisesOnTraining
from tests.conftest import make_test_http_request


@pytest.mark.asyncio
async def test_create_training_plan_successfully(
    create_customer,
    db,
    mock_send_push_notification,
):
    muscle_groups = await db.execute(
        select(MuscleGroup).options(selectinload(MuscleGroup.exercises))
    )

    training_plan_data = {
        "start_date": date.today().strftime('%Y-%m-%d'),
        "end_date": (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
        "diets": [
            {
                "proteins": 200,
                "fats": 100,
                "carbs": 400
            }
        ],
        "set_rest": 60,
        "exercise_rest": 120
    }

    trainings = []
    for muscle in muscle_groups.scalars():
        trainings.append({
            "name": muscle.name,
            "exercises": [
                dict(id=str(exercise.id), sets=[12, 12, 12], supersets=[])
                for exercise in muscle.exercises
            ]
        })

    training_plan_data["trainings"] = trainings

    response = await make_test_http_request(
        url=f"/api/customers/{create_customer.id}/training_plans",
        method="post",
        username=create_customer.coach.username,
        json=training_plan_data
    )

    status_code = response.status_code
    assert status_code == 201

    response = response.json()
    assert "id" in response
    assert response["number_of_trainings"] == len(training_plan_data["trainings"])
    # we expect to get strings because of design UI.
    # training plan card contains string conc.
    assert response["proteins"] == str(training_plan_data["diets"][0]["proteins"])
    assert response["fats"] == str(training_plan_data["diets"][0]["fats"])
    assert response["carbs"] == str(training_plan_data["diets"][0]["carbs"])

    # test that we have correct calories calculations
    d = training_plan_data["diets"][0]
    expected_calories = (d["proteins"] * 4) + (d["fats"] * 9) + (d["carbs"] * 4)
    assert response["calories"] == str(expected_calories)

    # check that we called firebase notification service with correct args
    assert create_customer.fcm_token in mock_send_push_notification.call_args.args
    excepted_push_notification_sent_data = {
        "title": "Создан новый тренировочный план",
        "body": f"с {training_plan_data['start_date']} до {training_plan_data['end_date']}",
    }
    assert excepted_push_notification_sent_data in mock_send_push_notification.call_args.args


@pytest.mark.asyncio
async def test_create_training_plan_with_supersets_successfully(
    create_customer,
    db,
    mock_send_push_notification,
):
    muscle_groups = await db.execute(
        select(MuscleGroup).options(selectinload(MuscleGroup.exercises))
    )

    training_plan_data = {
        "start_date": date.today().strftime('%Y-%m-%d'),
        "end_date": (date.today() + timedelta(days=7)).strftime('%Y-%m-%d'),
        "diets": [
            {
                "proteins": 200,
                "fats": 100,
                "carbs": 400
            }
        ],
        "set_rest": 60,
        "exercise_rest": 120
    }

    trainings = []
    for muscle in muscle_groups.scalars():
        trainings.append({
            "name": muscle.name,
            "exercises": [dict(id=str(exercise.id), sets=[12, 12, 12], supersets=[]) for exercise in muscle.exercises],
        })

    training_plan_data["trainings"] = trainings

    # link exercises to supersets:

    # first superset
    first_exercise_id_in_superset = training_plan_data["trainings"][0]["exercises"][0]["id"]
    second_exercise_id_in_superset = training_plan_data["trainings"][0]["exercises"][1]["id"]

    training_plan_data["trainings"][0]["exercises"][0]["supersets"].append(second_exercise_id_in_superset)
    training_plan_data["trainings"][0]["exercises"][1]["supersets"].append(first_exercise_id_in_superset)

    # second superset is tri-set
    first_exercise_id_in_triset = training_plan_data["trainings"][1]["exercises"][0]["id"]
    second_exercise_id_in_triset = training_plan_data["trainings"][1]["exercises"][1]["id"]
    third_exercise_id_in_triset = training_plan_data["trainings"][1]["exercises"][2]["id"]

    training_plan_data["trainings"][1]["exercises"][0]["supersets"].append(second_exercise_id_in_triset)
    training_plan_data["trainings"][1]["exercises"][0]["supersets"].append(third_exercise_id_in_triset)

    training_plan_data["trainings"][1]["exercises"][1]["supersets"].append(first_exercise_id_in_triset)
    training_plan_data["trainings"][1]["exercises"][1]["supersets"].append(third_exercise_id_in_triset)

    training_plan_data["trainings"][1]["exercises"][2]["supersets"].append(first_exercise_id_in_triset)
    training_plan_data["trainings"][1]["exercises"][2]["supersets"].append(second_exercise_id_in_triset)

    response = await make_test_http_request(
        url=f"/api/customers/{create_customer.id}/training_plans",
        method="post",
        username=create_customer.coach.username,
        json=training_plan_data
    )

    assert response.status_code == 201

    # check that we called firebase notification service with correct args
    assert create_customer.fcm_token in mock_send_push_notification.call_args.args
    excepted_push_notification_sent_data = {
        "title": "Создан новый тренировочный план",
        "body": f"с {training_plan_data['start_date']} до {training_plan_data['end_date']}",
    }
    assert excepted_push_notification_sent_data in mock_send_push_notification.call_args.args

    superset_exercises_ids = (
        first_exercise_id_in_superset,
        second_exercise_id_in_superset
    )
    exercises_in_superset = await db.execute(
        select(ExercisesOnTraining).where(
            ExercisesOnTraining.exercise_id.in_(superset_exercises_ids)
        )
    )

    s = set()
    for e in exercises_in_superset.scalars():
        s.add(e.superset_id)

    # exercises have the same superset_id
    assert len(s) == 1
    s.clear()

    triset_exercises_ids = (
        first_exercise_id_in_triset,
        second_exercise_id_in_triset,
        third_exercise_id_in_triset
    )
    exercises_in_triset = await db.execute(
        select(ExercisesOnTraining).where(
            ExercisesOnTraining.exercise_id.in_(triset_exercises_ids)
        )
    )

    for e in exercises_in_triset.scalars():
        s.add(e.superset_id)

    # exercises have the same superset_id
    assert len(s) == 1

    if response.status_code == 201:
        await db.execute(
            delete(TrainingPlan).where(TrainingPlan.id == response.json()["id"])
        )
        await db.commit()

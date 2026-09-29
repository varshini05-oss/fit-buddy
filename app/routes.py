from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from .database import (
    get_all_plans,
    get_all_users,
    get_original_plan,
    save_plan,
    save_user,
    update_plan,
)
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput, WorkoutRequest
from .updated_plan import update_workout_plan

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@router.post("/generate-workout")
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        user_data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity,
        )

        plan = generate_workout_gemini(user_data.model_dump())
        nutrition_tip = generate_nutrition_tip_with_flash(user_data.goal)

        save_plan(user_data.user_id, plan)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "username": user_data.username,
                "user_id": user_data.user_id,
                "age": user_data.age,
                "weight": user_data.weight,
                "goal": user_data.goal,
                "intensity": user_data.intensity,
                "workout_plan": plan,
                "nutrition_tip": nutrition_tip,
                "updated_plan": None,
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/submit-feedback")
async def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
):
    original = get_original_plan(user_id)

    if not original:
        raise HTTPException(
            status_code=404,
            detail="Original plan not found for this user.",
        )

    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)

    user = __import__("app.database", fromlist=["get_user"]).get_user(user_id)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
                        "username": user.name if user else "User",
                        "user_id": user_id,
                        "age": user.age if user else "",
                        "weight": user.weight if user else "",
                        "goal": user.goal if user else "",
                        "intensity": user.intensity if user else "",
                        "workout_plan": original,
                        "nutrition_tip": generate_nutrition_tip_with_flash(user.goal) if user else "",
                        "updated_plan": updated,
                        "feedback_submitted": True
        }
    )


@router.get("/view-all-users")
async def view_all_users(request: Request):
    users = get_all_users()
    plans = get_all_plans()

    plan_map = {
        plan.user_id: plan
        for plan in plans
    }

    users_data = []
    for user in users:
        plan = plan_map.get(user.user_id)
        users_data.append(
            {
                "user_id": user.user_id,
                "name": user.name,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated",
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users_data,
        }
        # "all_users.html",
        # {
        #     "request": request,
        #     "users": users_data,
        # },
    )


@router.post("/api/generate-workout")
async def api_generate_workout(payload: WorkoutRequest):
    plan = generate_workout_gemini(payload.model_dump())
    return JSONResponse(
        {
            "model": "gemini-1.5-pro",
            "workout_plan": plan,
        }
    )


@router.get("/api/nutrition-tip")
async def api_nutrition_tip(goal: str):
    tip = generate_nutrition_tip_with_flash(goal)
    return JSONResponse(
        {
            "model": "gemini-1.5-flash",
            "goal": goal,
            "nutrition_tip": tip,
        }
    )


@router.post("/api/generate-plan")
async def api_generate_plan(payload: UserInput):
    save_user(
        user_id=payload.user_id,
        name=payload.username,
        age=payload.age,
        weight=payload.weight,
        goal=payload.goal,
        intensity=payload.intensity,
    )

    plan = generate_workout_gemini(payload.model_dump())
    tip = generate_nutrition_tip_with_flash(payload.goal)
    save_plan(payload.user_id, plan)

    return {
        "message": "Workout plan generated and saved successfully",
        "workout_plan": plan,
        "nutrition_tip": tip,
    }


@router.post("/api/submit-feedback")
async def api_submit_feedback(payload: FeedbackRequest):
    original = get_original_plan(payload.user_id)

    if not original:
        raise HTTPException(
            status_code=404,
            detail="Original plan not found for this user.",
        )

    updated = update_workout_plan(original, payload.feedback)
    update_plan(payload.user_id, updated)

    return {
        "message": "Workout plan updated successfully",
        "updated_plan": updated,
    }

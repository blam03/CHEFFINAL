# from fastapi import APIRouter, Depends
# from pydantic import BaseModel
# from typing import List, Optional
# from app.services.ai_prompt import generate_meal_plan
# from app.services.user_store import get_user_preferences
# from app.services.auth import verify_token


# router = APIRouter()

# class CalendarEvent(BaseModel):
#     start: str
#     end: str
#     summary: Optional[str] = ""

# class MealPlanRequest(BaseModel):
#     user_id: str
#     events: List[CalendarEvent]

# # @router.post("/generate")
# # def generate_plan(data: MealPlanRequest):
# #     # Placeholder: mock user preferences for now
# #     user_preferences = {
# #         "meal_goal": "maintain weight",
# #         "dietary_restrictions": "none",
# #         "favorite_cuisines": ["Italian", "Mexican"],
# #         "preferred_meal_times": ["08:00", "13:00", "19:00"],
# #         "daily_calories": 2000,
# #         "allergies": [],
# #         "max_time_minutes": 30,
# #         "meals_per_day": 3
# #     }

# #     meal_plan = generate_meal_plan(data.events, user_preferences)
# #     return {"meal_plan": meal_plan}

# @router.post("/generate")
# def generate_plan(data: MealPlanRequest, decoded_token: dict = Depends(verify_token)):
#     user_id = decoded_token["uid"]

#     prefs = get_user_preferences(user_id)
#     if not prefs:
#         return {"error": "User preferences not found"}

#     meal_plan = generate_meal_plan(data.events, prefs.dict())
#     return {"meal_plan": meal_plan}

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.services.auth import verify_token
from app.services.user_store import get_user_preferences
from app.services.ai_prompt import generate_meal_plan
from app.services.meal_plan_store import save_meal_plan, get_meal_history
from datetime import datetime

router = APIRouter()

class CalendarEvent(BaseModel):
    start: str
    end: str
    summary: Optional[str] = ""

class MealPlanRequest(BaseModel):
    events: List[CalendarEvent]

@router.post("/generate")
def generate_plan(data: MealPlanRequest, decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token["uid"]
    prefs = get_user_preferences(user_id)

    if not prefs:
        return {"error": "User preferences not found. Please save them first."}

    # 🧠 New: Fetch meal history
    history = get_meal_history(user_id)

    # 📋 Generate meal plan with awareness of history
    meal_plan = generate_meal_plan(data.events, prefs.dict(), meal_history=history)

    # Save meal plan
    today = datetime.utcnow().strftime("%Y-%m-%d")
    save_meal_plan(user_id, today, meal_plan)

    return {"meal_plan": meal_plan}

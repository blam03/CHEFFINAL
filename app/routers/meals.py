from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.ai_prompt import generate_meal_ideas

router = APIRouter()

class MealPreferences(BaseModel):
    meal_goal: Optional[str] = None  # weight loss, muscle gain, maintain weight
    dietary_restrictions: Optional[str] = None  # vegetarian, vegan, keto, etc.
    favorite_cuisines: Optional[List[str]] = []
    preferred_meal_times: Optional[List[str]] = []  # e.g., ["08:00", "13:00", "19:00"]
    daily_calories: Optional[int] = None
    allergies: Optional[List[str]] = []
    max_time_minutes: Optional[int] = 30
    meals_per_day: Optional[int] = 3

@router.post("/suggestions")
def suggest_meals(preferences: MealPreferences):
    ideas = generate_meal_ideas(preferences)
    return {
        "suggested_meals": ideas
    }

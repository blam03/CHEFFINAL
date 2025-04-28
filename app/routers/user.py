from pydantic import BaseModel
from fastapi import APIRouter, Depends
from app.routers.meals import MealPreferences
from app.services.user_store import get_user_preferences, save_user_preferences
from app.services.auth import verify_token
from app.services.meal_plan_store import get_meal_history
from app.services.grocery_list import generate_grocery_list
from app.services.analytics import generate_user_analytics


router = APIRouter()

class SavePreferencesRequest(BaseModel):
    preferences: MealPreferences

@router.post("/user/save-preferences")
def save_preferences(data: SavePreferencesRequest, decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token["uid"]
    save_user_preferences(user_id, data.preferences)
    return {"message": "Preferences saved successfully ✅"}

@router.get("/user/get-preferences")
def get_preferences(decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token["uid"]
    prefs = get_user_preferences(user_id)
    if prefs:
        return {"preferences": prefs.dict()}
    else:
        return {"preferences": None}
    

@router.get("/user/get-meal-history")
def get_meal_history_endpoint(decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token["uid"]
    history = get_meal_history(user_id)
    return {"meal_history": history}


@router.get("/user/grocery-list")
def get_grocery_list(decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token["uid"]
    grocery_list = generate_grocery_list(user_id)
    return {"grocery_list": grocery_list}

@router.get("/user/analytics")
def get_user_analytics(decoded_token: dict = Depends(verify_token)):
    user_id = decoded_token["uid"]
    analytics = generate_user_analytics(user_id)
    return {"analytics": analytics}
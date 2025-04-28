from app.routers.meals import MealPreferences
from app.services.firebase import db

def save_user_preferences(user_id: str, prefs: MealPreferences):
    doc_ref = db.collection("users").document(user_id)
    doc_ref.set(prefs.dict())

def get_user_preferences(user_id: str) -> MealPreferences:
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        return MealPreferences(**doc.to_dict())
    return None

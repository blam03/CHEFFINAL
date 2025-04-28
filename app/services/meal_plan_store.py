from app.services.firebase import db

def save_meal_plan(user_id: str, date: str, meal_plan: list):
    structured_meals = []

    for item in meal_plan:
        parts = item.split(" - ")
        if len(parts) == 4:
            time, meal_name, calories_text, tags_text = parts

            # 🧠 New: Clean calories before converting
            calories_clean = calories_text.lower().replace("calories", "").replace("~", "").strip()
            try:
                calories = int(calories_clean)
            except ValueError:
                calories = None  # fallback if AI outputs weird format

            tags = tags_text.strip("[]").split(", ")
            structured_meals.append({
                "time": time,
                "meal_name": meal_name,
                "calories": calories,
                "tags": tags
            })
        else:
            structured_meals.append({"raw": item})

    doc_ref = db.collection("users").document(user_id).collection("mealPlans").document(date)
    doc_ref.set({
        "meal_plan": structured_meals
    })


def get_meal_history(user_id: str):
    meal_plans_ref = db.collection("users").document(user_id).collection("mealPlans")
    docs = meal_plans_ref.stream()

    history = []
    for doc in docs:
        history.append({
            "date": doc.id,
            "meal_plan": doc.to_dict().get("meal_plan", [])
        })
    
    return history

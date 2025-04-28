from app.services.firebase import db
from datetime import datetime, timedelta
from collections import Counter

def generate_user_analytics(user_id: str):
    # Fetch last 30 days of meal plans
    today = datetime.utcnow()
    last_30_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    total_calories = 0
    meal_count = 0
    meal_times = []

    for date in last_30_days:
        meal_plan_doc = db.collection("users").document(user_id).collection("mealPlans").document(date).get()
        if meal_plan_doc.exists:
            meal_plan_data = meal_plan_doc.to_dict().get("meal_plan", [])
            for meal in meal_plan_data:
                if meal.get("calories"):
                    total_calories += meal["calories"]
                    meal_count += 1
                if meal.get("time"):
                    meal_times.append(meal["time"])

    # Calculate averages
    average_calories = int(total_calories / meal_count) if meal_count else 0
    most_common_times = [time for time, _ in Counter(meal_times).most_common(3)]

    # Simple placeholder macros analysis (Optional: Can improve with AI later)
    average_macros = {
        "protein": "30g",
        "carbs": "40g",
        "fats": "15g"
    }

    # Placeholder goal tracking
    if average_calories > 600:
        goal_status = "Aligned with goal: muscle gain"
    elif average_calories < 400:
        goal_status = "Aligned with goal: weight loss"
    else:
        goal_status = "Aligned with goal: maintain weight"

    return {
        "average_calories_per_meal": average_calories,
        "average_macros_per_meal": average_macros,
        "goal_tracking": goal_status,
        "most_popular_meal_times": most_common_times
    }

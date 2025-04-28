from app.services.firebase import db
from datetime import datetime
from app.services.ai_prompt import model

def generate_grocery_list(user_id: str):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    meal_plan_doc = db.collection("users").document(user_id).collection("mealPlans").document(today).get()

    if not meal_plan_doc.exists:
        return ["No meal plan found for today."]

    meal_plan_data = meal_plan_doc.to_dict()
    meal_plan = meal_plan_data.get("meal_plan", [])

    # Build list of meal names
    meal_names = [meal.get("meal_name") for meal in meal_plan if "meal_name" in meal]

    if not meal_names:
        return ["No meals found for today."]

    # Build the AI prompt
    prompt = f"""
    Given the following meals planned for today, list all ingredients needed. 
    Group similar ingredients together and avoid duplication.

    Meals:
    {', '.join(meal_names)}

    Return a simple bullet point list of ingredients only.
    """

    try:
        response = model.generate_content(prompt)
        grocery_list = response.text.strip().splitlines()
        return grocery_list
    except Exception as e:
        return [f"Error generating grocery list: {str(e)}"]

import google.generativeai as genai
import os

genai.configure(api_key="---")
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

def generate_meal_times(events: list, meals_per_day: int = 3):
    formatted_events = "\n".join([
        f"- {e['summary']} from {e['start']} to {e['end']}"
        for e in events
    ])

    prompt = f"""
    Given the following calendar events, suggest {meals_per_day} optimal meal times
    (breakfast, lunch, dinner) that do not conflict with these events:

    Events:
    {formatted_events}

    Return a list of times in 24-hour format, one per line.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip().splitlines()
    except Exception as e:
        return [f"Error from Gemini: {str(e)}"]
    

def generate_meal_ideas(preferences):
    prompt_parts = [
        f"Suggest {preferences.meals_per_day or 3} meals based on the following user preferences:"
    ]

    if preferences.meal_goal:
        prompt_parts.append(f"- Goal: {preferences.meal_goal}")

    if preferences.dietary_restrictions:
        prompt_parts.append(f"- Dietary restrictions: {preferences.dietary_restrictions}")

    if preferences.favorite_cuisines:
        prompt_parts.append(f"- Favorite cuisines: {', '.join(preferences.favorite_cuisines)}")

    if preferences.preferred_meal_times:
        prompt_parts.append(f"- Preferred meal times: {', '.join(preferences.preferred_meal_times)}")

    if preferences.daily_calories:
        prompt_parts.append(f"- Target daily calories: {preferences.daily_calories}")

    if preferences.allergies:
        prompt_parts.append(f"- Avoid ingredients: {', '.join(preferences.allergies)}")

    if preferences.max_time_minutes:
        prompt_parts.append(f"- Max cooking time: {preferences.max_time_minutes} minutes")

    prompt_parts.append("Return a simple list of meal names, one per line. Do not include descriptions or calories.")

    prompt = "\n".join(prompt_parts)

    try:
        response = model.generate_content(prompt)
        return response.text.strip().splitlines()
    except Exception as e:
        return [f"Error from Gemini: {str(e)}"]



def generate_meal_plan(events: list, preferences: dict, meal_history: list = None):
    formatted_events = "\n".join([
        f"- {e.start} to {e.end}: {e.summary or 'Busy'}"
        for e in events
    ])

    # 🧠 New: Build recent meals list if available
    recent_meals_text = ""
    if meal_history:
        recent_meals = []
        for day in meal_history:
            for meal in day["meal_plan"]:
                if "meal_name" in meal:
                    recent_meals.append(meal["meal_name"])
        
        if recent_meals:
            recent_meals_text = (
                "\nAvoid suggesting these meals again (user had them recently):\n" +
                "\n".join([f"- {meal}" for meal in recent_meals])
            )
    
    # 🛠 Build the full AI prompt
    prompt = f"""
You are a meal planning assistant.

**The user is unavailable during the following times today (busy events):**
{formatted_events}

**Busy times mean the user cannot eat during these times.**
git 
**User Preferences:**
- Meal Goal: {preferences['meal_goal']}
- Dietary Restrictions: {preferences['dietary_restrictions']}
- Favorite Cuisines: {', '.join(preferences['favorite_cuisines'])}
- Preferred Meal Times: {', '.join(preferences['preferred_meal_times'])}
- Target Daily Calories: {preferences['daily_calories']}
- Allergies: {', '.join(preferences['allergies'])}
- Max Cooking Time: {preferences['max_time_minutes']} minutes
- Meals Per Day: {preferences['meals_per_day']}

**Instructions:**
1. Find FREE time gaps outside of the busy event times.
2. Meals must be scheduled during these FREE GAPS ONLY.
3. Try to match the preferred meal times if possible (breakfast, lunch, dinner).
4. Output exactly {preferences['meals_per_day']} meals.
5. Each meal should include:
   - Meal Time (24h format)
   - Meal Name
   - Estimated Calories
   - Tags (quick, healthy, high-protein, vegetarian, etc.)

**Rules:**
- 🚫 NEVER schedule meals during busy events.
- ✅ ONLY suggest meals during free times.
- ✅ Match preferred eating windows when possible.

**Output Format (ONLY):**
[Meal Time 24-hour] - [Meal Name] - [Calories estimate] - [Tags]

**DO NOT write paragraphs, explanations, or anything else. Only the meal plan list.**
"""




    try:
        response = model.generate_content(prompt)
        return response.text.strip().splitlines()
    except Exception as e:
        return [f"Error from Gemini: {str(e)}"]

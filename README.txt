# CHEF Backend (Come Home Eat Fresh)

The FastAPI backend for CHEF — an AI-driven meal planner that personalizes meals based on:

- User preferences
- Calendar availability
- Past meal history

Connected to **Firebase Authentication** and **Firestore** for secure user management and data storage.

---

✅ API List:


Endpoint	            Method	Purpose
/user/save-preferences	POST	Save user's meal preferences
/user/get-preferences	GET	    Fetch user's saved preferences
/planner/generate	    POST	Generate a meal plan based on calendar events
/user/get-meal-history	GET	    Fetch past meal plans
/user/grocery-list	    GET	    Get grocery shopping list
/user/analytics	        GET	    Get user's analytics dashboard info

---

## 🚀 Features

- 🔒 Google Sign-In Authentication (Firebase Auth)
- 🔐 Secure Token Verification (`idToken`)
- 📝 Save and Fetch User Meal Preferences
- 🍽️ AI-Personalized Meal Plans (Google Gemini AI)
- 🗓️ Save Meal Plans by Date (Firestore)
- 🔄 Adaptive AI (based on user's past meal history)
- 🛒 Grocery List Generator based on today's planned meals

---

## 🏗️ Tech Stack

- FastAPI (Python 3.9+)
- Firebase Admin SDK (Firestore + Authentication)
- Google Gemini AI (Meal Planning + Grocery Lists)
- Swagger UI (for easy API testing)

---

## ⚙️ Running Locally

1. **Clone the repo**

2. **Set up a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```

3. **Add your `firebase_key.json`**

    Place your Firebase service account key JSON file in the project root directory.

4. **Start the server**

    ```bash
    python3 -m uvicorn app.main:app --reload
    ```

5. **Access API Documentation**

    Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔑 Authentication Flow

- Frontend (React) authenticates user with Firebase and retrieves an `idToken`.
- All secure API requests must include:

    ```
    Authorization: Bearer <idToken>
    ```

---

## 📚 API Endpoints

| Endpoint | Method | Purpose |
|:---------|:-------|:--------|
| `/user/save-preferences` | POST | Save user's meal preferences |
| `/user/get-preferences` | GET | Fetch user's saved preferences |
| `/planner/generate` | POST | Generate smart AI meal plan based on calendar + preferences |
| `/user/get-meal-history` | GET | Retrieve user's past meal plans |
| `/user/grocery-list` | GET | Generate a grocery shopping list for today's meals |

---

## 🧠 AI Usage

- **Meal Planning**:  
  Gemini suggests meals personalized to user's availability, preferences, and recent meal history.

- **Grocery List Generation**:  
  Gemini builds a simple ingredient list based on planned meals.

---

## 🔥 Notes

- User data is securely associated with their Firebase UID in Firestore.
- No sensitive credentials (like passwords) are stored manually.
- AI prompts are structured to prevent repetitive meal suggestions.

---





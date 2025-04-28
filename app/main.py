from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware


from app.routers import calendar, meals, chatbot, planner, test_firebase, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if you want to restrict to only frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bearer_scheme = HTTPBearer()
app.include_router(calendar.router, prefix="/calendar")
app.include_router(meals.router, prefix="/meals")
app.include_router(chatbot.router, prefix="/chatbot")
app.include_router(planner.router, prefix="/planner")
app.include_router(test_firebase.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "CHEF Backend is running 🚀"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CHEF Backend API",
        version="1.0.0",
        description="Backend API for CHEF app, with Google Auth and AI meal planning",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


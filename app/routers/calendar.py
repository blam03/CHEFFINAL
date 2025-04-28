from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.ai_prompt import generate_meal_times

router = APIRouter()

class CalendarEvent(BaseModel):
    start: str
    end: str
    summary: str = ""

@router.post("/events")
def suggest_meal_times(events: List[CalendarEvent]):
    event_data = [e.dict() for e in events]
    mealtimes = generate_meal_times(event_data)
    return {
        "received_events": len(events),
        "suggested_mealtimes": mealtimes
    }

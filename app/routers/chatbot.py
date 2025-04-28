from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def chatbot_reply(prompt: str):
    return {"response": f"Imagine an AI answered: {prompt}"}

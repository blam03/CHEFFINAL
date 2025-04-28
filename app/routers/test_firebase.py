from fastapi import APIRouter
from app.services.firebase import db

router = APIRouter()

@router.get("/firebase/test-write")
def test_write():
    db.collection("test").document("hello").set({"message": "Firebase is connected!"})
    return {"status": "Data written to Firestore ✅"}

@router.get("/firebase/test-read")
def test_read():
    doc = db.collection("test").document("hello").get()
    if doc.exists:
        return {"data": doc.to_dict()}
    else:
        return {"error": "Document not found"}

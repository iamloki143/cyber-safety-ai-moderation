from fastapi import APIRouter
from backend.schemas import TextInput
from models.text.inference import predict_text
from backend.db import moderation_logs
from datetime import datetime

router = APIRouter()

@router.post("/text-check")
def check_text(data: TextInput):

    result = predict_text(data.text)

    record = {
        "type": "text",
        "user_id": data.user_id,
        "content": data.text,
        "language": result["language"],
        "category": result["category"],
        "confidence": result["confidence"],
        "status": "blocked" if result["category"] == "Bullying" else "allowed",
        "timestamp": datetime.utcnow()
    }

    moderation_logs.insert_one(record)

    return result
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PredictionResponse(BaseModel):
    match_id: str
    win_probability: float
    confidence_level: str
    key_factors: list
    uncertainty_flags: list

@router.get("/upcoming")
async def get_upcoming(days: int = 7):
    return []

@router.get("/{match_id}")
async def get_match_prediction(match_id: str):
    return {}

@router.post("/manual")
async def manual_prediction(data: dict):
    return {}

@router.get("/high-confidence")
async def get_high_confidence(min_confidence: str = "HIGH", hours: int = 48):
    return []

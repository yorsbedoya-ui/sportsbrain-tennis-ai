import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

api_main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import predictions, results, accuracy, players, alerts

app = FastAPI(title="SportsBrain AI - Tennis", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictions.router, prefix="/tennis/predictions", tags=["Predictions"])
app.include_router(results.router, prefix="/tennis/results", tags=["Results"])
app.include_router(accuracy.router, prefix="/tennis/accuracy", tags=["Accuracy"])
app.include_router(players.router, prefix="/tennis/players", tags=["Players"])
app.include_router(alerts.router, prefix="/tennis/alerts", tags=["Alerts"])

@app.get("/")
def root():
    return {"status": "SportsBrain AI Tennis API Online"}
"""

api_predictions_content = """from fastapi import APIRouter
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
"""

write_file("api/main.py", api_main_content)
write_file("api/routers/__init__.py", "")
write_file("api/routers/predictions.py", api_predictions_content)
write_file("api/routers/results.py", "from fastapi import APIRouter\\nrouter = APIRouter()")
write_file("api/routers/accuracy.py", "from fastapi import APIRouter\\nrouter = APIRouter()")
write_file("api/routers/players.py", "from fastapi import APIRouter\\nrouter = APIRouter()")
write_file("api/routers/alerts.py", "from fastapi import APIRouter\\nrouter = APIRouter()")
write_file("api/schemas.py", "# Pydantic schemas for the API\\n")
write_file("api/auth.py", "# JWT Auth setup\\n")

print("API files generated.")

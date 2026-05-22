from fastapi import FastAPI
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

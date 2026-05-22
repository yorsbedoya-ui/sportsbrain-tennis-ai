import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

docker_compose = """version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: sportsbrain
      POSTGRES_PASSWORD: sportsbrain_pwd
      POSTGRES_DB: sportsbrain_tennis
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

  api:
    build: .
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    env_file: .env

  worker:
    build: .
    command: celery -A data_ingestion.tennis.scheduler worker -c 4 --loglevel=info
    depends_on:
      - redis
      - postgres
    env_file: .env

  beat:
    build: .
    command: celery -A data_ingestion.tennis.scheduler beat --loglevel=info
    depends_on:
      - redis
    env_file: .env

  flower:
    image: mher/flower
    ports:
      - "5555:5555"
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

volumes:
  pgdata:
"""

requirements = """fastapi==0.111.0
sqlalchemy==2.0.30
alembic==1.13.1
xgboost==2.0.3
torch==2.3.0
scikit-learn==1.4.2
celery==5.4.0
redis==5.0.4
shap==0.45.0
optuna==3.6.1
beautifulsoup4==4.12.3
httpx==0.27.0
pydantic==2.7.1
uvicorn==0.29.0
psycopg2-binary==2.9.9
pandas==2.2.2
"""

env_example = """DATABASE_URL=postgresql://sportsbrain:sportsbrain_pwd@postgres:5432/sportsbrain_tennis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
SECRET_KEY=super-secret-key-change-in-prod
ATP_API_KEY=your_atp_key
WTA_API_KEY=your_wta_key
OPENWEATHER_API_KEY=your_weather_key
SENTRY_DSN=your_sentry_dsn
MODEL_STORAGE_PATH=/app/models
"""

readme = """# SportsBrain AI - Tennis Module

Setup in 5 commands:
1. `git clone <repo>`
2. `cp .env.example .env`
3. `docker-compose up -d`
4. `python -c 'from data_ingestion.tennis.historical_loader import HistoricalDataLoader; HistoricalDataLoader(None).load_atp_historical(30)'`
5. Access API at `http://localhost:8000/docs`
"""

write_file("docker-compose.yml", docker_compose)
write_file("requirements.txt", requirements)
write_file(".env.example", env_example)
write_file("README.md", readme)
write_file("Dockerfile", "FROM python:3.11-slim\\nWORKDIR /app\\nCOPY requirements.txt .\\nRUN pip install -r requirements.txt\\nCOPY . .\\n")

print("Infra files generated.")

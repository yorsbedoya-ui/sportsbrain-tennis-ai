import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

os.makedirs("db/migrations/versions", exist_ok=True)

models_content = """import enum
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Date, Text, JSON
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

Base = declarative_base()

class Hand(str, enum.Enum):
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    AMBIDEXTROUS = "AMBIDEXTROUS"

class RoundEnum(str, enum.Enum):
    R128 = "R128"
    R64 = "R64"
    R32 = "R32"
    R16 = "R16"
    QF = "QF"
    SF = "SF"
    F = "F"

class SurfaceEnum(str, enum.Enum):
    CLAY = "CLAY"
    GRASS = "GRASS"
    HARD = "HARD"
    CARPET = "CARPET"

class MatchStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    LIVE = "LIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TourneyCategory(str, enum.Enum):
    GRAND_SLAM = "GRAND_SLAM"
    MASTERS_1000 = "MASTERS_1000"
    ATP500 = "ATP500"
    ATP250 = "ATP250"
    WTA1000 = "WTA1000"
    WTA500 = "WTA500"
    WTA250 = "WTA250"

class ConfidenceLevel(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    VERY_LOW = "VERY_LOW"

class ErrorType(str, enum.Enum):
    RANDOM = "RANDOM"
    STRUCTURAL = "STRUCTURAL"
    DATA_QUALITY = "DATA_QUALITY"

class ModelName(str, enum.Enum):
    XGBOOST = "XGBOOST"
    LSTM = "LSTM"
    BAYESIAN = "BAYESIAN"
    ENSEMBLE = "ENSEMBLE"

class TriggerReason(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    THRESHOLD = "THRESHOLD"
    MANUAL = "MANUAL"

class Player(Base):
    __tablename__ = 'players_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    nationality = Column(String)
    date_of_birth = Column(Date)
    hand = Column(String)
    atp_wta_id = Column(String, unique=True, index=True)
    turned_pro_year = Column(Integer)
    active = Column(Boolean, default=True)
    current_rank = Column(Integer)
    peak_rank = Column(Integer)
    peak_rank_date = Column(Date)
    coach_name = Column(String)
    coach_since_date = Column(Date)
    height_cm = Column(Integer)
    weight_kg = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Venue(Base):
    __tablename__ = 'venues_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    city = Column(String)
    country = Column(String)
    altitude_meters = Column(Float)
    capacity = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)

class Tournament(Base):
    __tablename__ = 'tournaments_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surface = Column(String)
    category = Column(String)
    country = Column(String)
    city = Column(String)
    venue_id = Column(UUID(as_uuid=True), ForeignKey('venues_tennis.id'))
    prize_money_usd = Column(Float)
    indoor = Column(Boolean)
    start_date = Column(Date)
    end_date = Column(Date)
    atp_wta_tournament_id = Column(String, index=True)

class Match(Base):
    __tablename__ = 'matches_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tournament_id = Column(UUID(as_uuid=True), ForeignKey('tournaments_tennis.id'), index=True)
    round = Column(String)
    player1_id = Column(UUID(as_uuid=True), ForeignKey('players_tennis.id'), index=True)
    player2_id = Column(UUID(as_uuid=True), ForeignKey('players_tennis.id'), index=True)
    winner_id = Column(UUID(as_uuid=True), ForeignKey('players_tennis.id'), nullable=True)
    surface = Column(String, index=True)
    date = Column(Date, index=True)
    start_time = Column(DateTime)
    venue_id = Column(UUID(as_uuid=True), ForeignKey('venues_tennis.id'))
    indoor = Column(Boolean)
    best_of = Column(Integer)
    status = Column(String, default="SCHEDULED")
    atp_wta_match_id = Column(String, index=True)

class MatchScore(Base):
    __tablename__ = 'match_scores_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches_tennis.id'), index=True)
    set_number = Column(Integer)
    player1_games = Column(Integer)
    player2_games = Column(Integer)
    player1_tiebreak = Column(Integer, nullable=True)
    player2_tiebreak = Column(Integer, nullable=True)
    duration_minutes = Column(Integer)

class PlayerStats(Base):
    __tablename__ = 'player_stats_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player_id = Column(UUID(as_uuid=True), ForeignKey('players_tennis.id'), index=True)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches_tennis.id'), index=True)
    date = Column(Date, index=True)
    surface = Column(String)
    tournament_id = Column(UUID(as_uuid=True), ForeignKey('tournaments_tennis.id'))
    aces = Column(Integer)
    double_faults = Column(Integer)
    first_serve_in_pct = Column(Float)
    first_serve_won_pct = Column(Float)
    second_serve_won_pct = Column(Float)
    break_points_faced = Column(Integer)
    break_points_saved = Column(Integer)
    break_points_opportunities = Column(Integer)
    break_points_converted = Column(Integer)
    service_games_played = Column(Integer)
    return_games_played = Column(Integer)
    return_points_won_pct = Column(Float)
    total_points_won = Column(Integer)
    winners = Column(Integer)
    unforced_errors = Column(Integer)
    net_points_won_pct = Column(Float)
    rank_at_match_time = Column(Integer)
    fatigue_score = Column(Float)
    travel_distance_km_last_7d = Column(Float)
    matches_played_last_21d = Column(Integer)

class Prediction(Base):
    __tablename__ = 'predictions_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches_tennis.id'), index=True)
    model_version = Column(String)
    sub_model_id = Column(UUID(as_uuid=True), ForeignKey('sub_models_tennis.id'), nullable=True)
    predicted_winner_id = Column(UUID(as_uuid=True), ForeignKey('players_tennis.id'))
    win_probability = Column(Float)
    set_score_prediction = Column(JSON)
    confidence_level = Column(String)
    key_factors = Column(JSON)
    uncertainty_flags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    model_accuracy_at_time = Column(Float)

class Result(Base):
    __tablename__ = 'results_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches_tennis.id'), unique=True)
    actual_winner_id = Column(UUID(as_uuid=True), ForeignKey('players_tennis.id'))
    actual_score_json = Column(JSON)
    duration_minutes = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String)

class EpisodicMemory(Base):
    __tablename__ = 'episodic_memory_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches_tennis.id'), index=True)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey('predictions_tennis.id'))
    error_delta = Column(Float)
    error_type = Column(String)
    error_classification_reason = Column(Text)
    conditions_snapshot = Column(JSON)
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelWeight(Base):
    __tablename__ = 'model_weights_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String)
    weights_json = Column(JSON)
    hyperparams_json = Column(JSON)
    accuracy_7d = Column(Float)
    accuracy_30d = Column(Float)
    accuracy_90d = Column(Float)
    accuracy_alltime = Column(Float)
    brier_score_30d = Column(Float)
    calibration_error_30d = Column(Float)
    training_samples_count = Column(Integer)
    version = Column(Integer, autoincrement=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SubModel(Base):
    __tablename__ = 'sub_models_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    trigger_condition = Column(JSON)
    trigger_threshold = Column(Float)
    model_type = Column(String)
    model_blob_path = Column(String)
    accuracy = Column(Float)
    sample_size = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_evaluated_at = Column(DateTime)

class ModelTrainingLog(Base):
    __tablename__ = 'model_training_log_tennis'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String)
    trigger_reason = Column(String)
    training_samples = Column(Integer)
    validation_accuracy = Column(Float)
    test_accuracy = Column(Float)
    training_duration_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
"""

database_content = """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sportsbrain:sportsbrain_pwd@localhost:5432/sportsbrain")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

write_file("db/models.py", models_content)
write_file("db/database.py", database_content)
print("Database schema generated.")

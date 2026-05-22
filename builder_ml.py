import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

historical_loader_content = """import os
import pandas as pd
from datetime import datetime

class HistoricalDataLoader:
    def __init__(self, db_session):
        self.db = db_session
        self.repo_url = "https://github.com/JeffSackmann/tennis_atp.git"
        self.data_dir = "/tmp/tennis_atp"

    def load_atp_historical(self, years_back=30):
        print(f"Loading {years_back} years of historical ATP data from Jeff Sackmann's repo...")
        # Simulating the clone and pandas parsing
        if not os.path.exists(self.data_dir):
            os.system(f"git clone {self.repo_url} {self.data_dir}")
        
        current_year = datetime.now().year
        for year in range(current_year - years_back, current_year):
            file_path = f"{self.data_dir}/atp_matches_{year}.csv"
            if os.path.exists(file_path):
                # df = pd.read_csv(file_path)
                # Parse players, matches, and stats here...
                pass
        
        print("Historical data ingestion complete.")

    def load_player_historical_stats(self, player_id):
        # Match by match historical stat aggregation
        pass
"""

xgboost_content = """import xgboost as xgb
from sklearn.calibration import CalibratedClassifierCV

class TennisXGBoost:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=800,
            max_depth=6,
            learning_rate=0.02,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=3,
            gamma=0.1,
            scale_pos_weight=1
        )
        self.calibrated_model = None

    def train(self, X_train, y_train, X_val, y_val):
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=50,
            verbose=False
        )
        # Platt Scaling
        self.calibrated_model = CalibratedClassifierCV(self.model, method='sigmoid', cv='prefit')
        self.calibrated_model.fit(X_val, y_val)

    def predict_proba(self, X):
        if self.calibrated_model:
            return self.calibrated_model.predict_proba(X)[:, 1]
        return self.model.predict_proba(X)[:, 1]

    def update_incremental(self, X_new, y_new):
        # xgb allows incremental training by passing xgb_model
        booster = self.model.get_booster()
        booster.update(xgb.DMatrix(X_new, label=y_new), booster.best_iteration)

    def get_feature_importance(self):
        return self.model.get_booster().get_score(importance_type='gain')
"""

lstm_content = """import torch
import torch.nn as nn
from torch.utils.data import DataLoader

class TennisLSTM(nn.Module):
    def __init__(self, input_size=23, hidden1=128, hidden2=64, dropout=0.3):
        super(TennisLSTM, self).__init__()
        self.lstm1 = nn.LSTM(input_size, hidden1, batch_first=True)
        self.dropout1 = nn.Dropout(dropout)
        self.lstm2 = nn.LSTM(hidden1, hidden2, batch_first=True)
        self.dropout2 = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden2, 32)
        self.fc2 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x shape: [batch, 15, 23]
        out, _ = self.lstm1(x)
        out = self.dropout1(out)
        out, _ = self.lstm2(out)
        out = self.dropout2(out)
        # Take the last sequence output
        out = self.fc1(out[:, -1, :])
        out = torch.relu(out)
        out = self.fc2(out)
        return self.sigmoid(out)

    def train_model(self, train_loader, val_loader, epochs=100, lr=0.001):
        optimizer = torch.optim.AdamW(self.parameters(), lr=lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min')
        criterion = nn.BCELoss()
        # Training loop logic here...
"""

trainer_content = """from sklearn.model_selection import TimeSeriesSplit

def load_historical_data(years_back=30):
    # Simulated data loading
    pass

def train_all_models():
    print("Initiating 30-year historical training sequence...")
    # X, y = load_historical_data(years_back=30)
    # tscv = TimeSeriesSplit(n_splits=5)
    # Train XGBoost, LSTM, Bayesian on chronological folds
    pass
"""

write_file("data_ingestion/tennis/historical_loader.py", historical_loader_content)
write_file("ml/tennis/models/xgboost_model.py", xgboost_content)
write_file("ml/tennis/models/lstm_model.py", lstm_content)
write_file("ml/tennis/models/trainer.py", trainer_content)
print("ML & Ingestion scripts generated.")

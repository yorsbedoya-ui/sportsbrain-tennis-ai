import xgboost as xgb
from sklearn.calibration import CalibratedClassifierCV

class BasketballXGBoost:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            max_depth=8,
            learning_rate=0.05,
            n_estimators=800,
            objective='binary:logistic',
            eval_metric='logloss'
        )
        self.calibrated_model = None

    def train(self, X_train, y_train, X_val, y_val):
        self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        self.calibrated_model = CalibratedClassifierCV(self.model, method='sigmoid', cv=2)
        self.calibrated_model.fit(X_val, y_val)

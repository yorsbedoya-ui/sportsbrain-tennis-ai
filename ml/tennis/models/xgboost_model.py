import xgboost as xgb
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

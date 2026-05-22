from sklearn.ensemble import RandomForestClassifier

class BasketballRandomForest:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=500, max_depth=12)
        
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

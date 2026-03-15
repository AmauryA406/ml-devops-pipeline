from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def train_model():
    iris = load_iris()
    X, y = iris.data, iris.target
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = train_model()
CLASSES = ["setosa", "versicolor", "virginica"]

def predict(features: list[float]) -> dict:
    X = np.array(features).reshape(1, -1)
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    return {
        "species": CLASSES[prediction],
        "confidence": round(float(proba[prediction]), 4)
    }
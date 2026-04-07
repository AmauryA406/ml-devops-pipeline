from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_setosa():
    response = client.post("/predict", json={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    assert response.json()["species"] == "setosa"
    assert response.json()["confidence"] == 1.0

def test_predict_returns_valid_species():
    response = client.post("/predict", json={
        "sepal_length": 6.3,
        "sepal_width": 3.3,
        "petal_length": 4.7,
        "petal_width": 1.6
    })
    assert response.status_code == 200
    assert response.json()["species"] in ["setosa", "versicolor", "virginica"]
    assert 0 <= response.json()["confidence"] <= 1
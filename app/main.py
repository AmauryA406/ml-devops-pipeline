from fastapi import FastAPI
from pydantic import BaseModel
from app.model import predict

app = FastAPI(title="Iris Classifier API", version="1.0.0")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionOutput(BaseModel):
    species: str
    confidence: float

@app.get("/")
def root():
    return {"status": "ok", "message": "Iris Classifier API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionOutput)
def make_prediction(input: IrisInput):
    features = [
        input.sepal_length,
        input.sepal_width,
        input.petal_length,
        input.petal_width
    ]
    result = predict(features)
    return result
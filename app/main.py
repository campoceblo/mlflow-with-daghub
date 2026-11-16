import os

import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_DIR = os.getenv("MODEL_DIR", "model")

app = FastAPI(title="Digits classifier")
model = mlflow.sklearn.load_model(MODEL_DIR)


class PredictRequest(BaseModel):
    # Each sample is an 8x8 digit image flattened to 64 pixel values (0-16)
    features: list[list[float]] = Field(..., min_length=1)


class PredictResponse(BaseModel):
    predictions: list[int]


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    predictions = model.predict(request.features)
    return PredictResponse(predictions=[int(p) for p in predictions])

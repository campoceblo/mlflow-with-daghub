# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fetch the latest trained model from DagsHub through MLflow.
# Credentials are passed as build secrets, so they are not stored in the image.
ARG MLFLOW_TRACKING_URI=https://dagshub.com/campoceblo/MLFlow-lab.mlflow
ARG MODEL_URI=models:/digits-classifier/latest
ENV MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI} \
    MODEL_URI=${MODEL_URI} \
    MODEL_DIR=/app/model
COPY download_model.py .
RUN --mount=type=secret,id=mlflow_username,env=MLFLOW_TRACKING_USERNAME \
    --mount=type=secret,id=mlflow_password,env=MLFLOW_TRACKING_PASSWORD \
    python download_model.py

COPY app/ app/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

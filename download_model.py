import os

import mlflow

MODEL_URI = os.getenv("MODEL_URI", "models:/digits-classifier/latest")
DEST = os.getenv("MODEL_DIR", "model")

path = mlflow.artifacts.download_artifacts(artifact_uri=MODEL_URI, dst_path=DEST)
print(f"Downloaded {MODEL_URI} to {path}")

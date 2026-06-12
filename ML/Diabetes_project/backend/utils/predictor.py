# Loads the SVM model and StandardScaler, runs scaled predictions on health metrics.

import json
import pickle
from pathlib import Path

import numpy as np

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"

with open(MODEL_DIR / "diabetes_prediction.pickle", "rb") as model_file:
    model = pickle.load(model_file)

with open(MODEL_DIR / "scaler.pickle", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

with open(MODEL_DIR / "columns.json") as columns_file:
    columns = json.load(columns_file)["data_columns"]


def validate_input(data):
    """Return (input_values, error_message) — error_message is None when valid."""
    if not data:
        return None, "Request body is required"

    missing = [col for col in columns if col not in data]
    if missing:
        return None, f"Missing fields: {', '.join(missing)}"

    input_values = []
    for col in columns:
        try:
            input_values.append(float(data[col]))
        except (TypeError, ValueError):
            return None, f"Field '{col}' must be a numeric value"

    return input_values, None


def predict(data):
    """Scale input features and return prediction label and numeric result."""
    input_values, error = validate_input(data)
    if error:
        return None, error

    input_array = np.array(input_values).reshape(1, -1)
    scaled = scaler.transform(input_array)
    prediction = int(model.predict(scaled)[0])
    label = "Diabetic" if prediction == 1 else "Not Diabetic"

    return {"prediction": prediction, "label": label}, None

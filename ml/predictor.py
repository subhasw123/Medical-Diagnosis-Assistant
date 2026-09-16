import os
import joblib
import numpy as np
import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="sklearn"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "disease_model.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "label_encoder.pkl"
)

model = None
encoder = None


def load_model():

    global model, encoder

    if model is None:
        print(f"Loading model from: {MODEL_PATH}")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}"
            )

        model = joblib.load(MODEL_PATH)

        print("Disease prediction model loaded successfully.")

    if encoder is None:
        print(f"Loading encoder from: {ENCODER_PATH}")

        if not os.path.exists(ENCODER_PATH):
            raise FileNotFoundError(
                f"Encoder file not found: {ENCODER_PATH}"
            )

        encoder = joblib.load(ENCODER_PATH)

        print("Label encoder loaded successfully.")


def predict_top3(vector):

    load_model()

    probabilities = model.predict_proba(
        np.array([vector])
    )[0]

    top_indices = np.argsort(probabilities)[-3:][::-1]

    best_probability = probabilities[top_indices[0]]

    predictions = []

    for idx in top_indices:

        disease = encoder.inverse_transform([idx])[0]

        if best_probability > 0:
            relative_confidence = round(
                (probabilities[idx] / best_probability) * 100,
                2
            )
        else:
            relative_confidence = 0.0

        predictions.append({
            "disease": disease,
            "confidence": float(relative_confidence),
            "raw_probability": float(
                round(probabilities[idx] * 100, 2)
            )
        })

    return predictions


def predict_disease(vector):

    predictions = predict_top3(vector)

    if not predictions:
        raise ValueError(
            "No predictions returned by model"
        )

    top_prediction = predictions[0]

    return (
        top_prediction["disease"],
        top_prediction["confidence"]
    )
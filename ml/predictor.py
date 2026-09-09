import joblib
import numpy as np
import warnings

# Suppress sklearn UserWarning about lacking feature names
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="sklearn"
)

# Model and encoder will be loaded only when needed
model = None
encoder = None


def load_model():

    global model, encoder

    if model is None or encoder is None:

        print("Loading disease prediction model...")

        model = joblib.load(
            "ml/models/disease_model.pkl"
        )

        encoder = joblib.load(
            "ml/models/label_encoder.pkl"
        )

        print("Disease prediction model loaded successfully.")


def predict_top3(vector):

    # Load model only when prediction is requested
    load_model()

    probabilities = model.predict_proba([vector])[0]

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
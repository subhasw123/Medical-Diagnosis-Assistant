import joblib
import numpy as np

model = joblib.load("ml/models/disease_model.pkl")
encoder = joblib.load("ml/models/label_encoder.pkl")


def predict_top3(vector):

    probabilities = model.predict_proba([vector])[0]

    top_indices = np.argsort(probabilities)[-3:][::-1]

    best_probability = probabilities[top_indices[0]]

    predictions = []

    for idx in top_indices:

        disease = encoder.inverse_transform([idx])[0]

        relative_confidence = round(
            (probabilities[idx] / best_probability) * 100,
            2
        )

        predictions.append({
            "disease": disease,
            "confidence": relative_confidence,
            "raw_probability": round(
                probabilities[idx] * 100,
                2
            )
        })

    return predictions


def predict_disease(vector):
    predictions = predict_top3(vector)

    if not predictions:
        raise ValueError("No predictions returned by model")

    top_prediction = predictions[0]
    return top_prediction["disease"], top_prediction["confidence"]

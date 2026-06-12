from ml.load_symptoms import SYMPTOMS
from ml.predictor import predict_top3
from database.diagnosis_queries import (
    save_patient,
    save_diagnosis
)
from ml.disease_info import DISEASE_INFO

def create_feature_vector(
    selected_symptoms
):

    vector = [0] * len(SYMPTOMS)

    for symptom in selected_symptoms:

        symptom = symptom.strip().lower()

        if symptom in SYMPTOMS:

            index = SYMPTOMS.index(symptom)

            vector[index] = 1

    return vector


class DiagnosisService:
    """Service for handling diagnosis requests"""
    
    def diagnose(self, data):
        """
        Diagnose based on symptoms
        
        Args:
            data: dict with keys - full_name, age, gender, symptoms (list)
        
        Returns:
            dict with disease and confidence
        """
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return {
                'error': 'No symptoms provided',
                'disease': None,
                'confidence': 0
            }
        
        # Create feature vector from symptoms
        vector = create_feature_vector(symptoms)
        
        # Get Top 3 predictions
        predictions = predict_top3(vector)

        for prediction in predictions:

            disease = prediction["disease"].lower()

            info = DISEASE_INFO.get(
                disease,
                {
                    "description": "Information not available.",
                    "advice": [
                        "Consult a healthcare professional."
                    ]
                }
            )

            prediction["description"] = info["description"]
            prediction["advice"] = info["advice"]
            
        patient_id = save_patient(
            data.get('full_name'),
            data.get('age'),
            data.get('gender')
        )

        best_prediction = predictions[0]

        save_diagnosis(
            patient_id,
            best_prediction["disease"],
            best_prediction["confidence"]
        )

        return {
            'full_name': data.get('full_name'),
            'age': data.get('age'),
            'gender': data.get('gender'),
            'symptoms': symptoms,
            'predictions': predictions
        }

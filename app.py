from flask import Flask
from flask import render_template
from flask import request

from ml.predictor import predict_disease
from services.diagnosis_service import (
    create_feature_vector
)
from routes.diagnosis_routes import diagnosis_bp
from routes.chatbot_routes import chatbot_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)


app.secret_key = "medical_diagnosis_secret"

# Register blueprints
app.register_blueprint(diagnosis_bp)
app.register_blueprint(admin_bp)

@app.route("/")
def home():
    return render_template(
        "diagnosis.html"
    )

app.register_blueprint(
    chatbot_bp
)

@app.route("/predict", methods=["POST"])
def predict():

    symptoms_text = request.form[
        "symptoms"
    ]

    symptoms = symptoms_text.split(",")

    vector = create_feature_vector(
        symptoms
    )

    disease, confidence = predict_disease(
        vector
    )

    return render_template(
        "result.html",
        disease=disease,
        confidence=round(confidence, 2)
    )

if __name__ == "__main__":
    app.run(debug=True)
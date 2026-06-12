from flask import Blueprint, request, jsonify
from services.diagnosis_service import DiagnosisService
from ml.load_symptoms import SYMPTOMS
from database.diagnosis_queries import (
    get_history
)
from flask import render_template

diagnosis_bp = Blueprint('diagnosis', __name__, url_prefix='/diagnosis')
service = DiagnosisService()

@diagnosis_bp.route('/history')
def history():

    rows = get_history()

    return render_template(
        "history.html",
        rows=rows
    )

@diagnosis_bp.route('/symptoms', methods=['GET'])
def get_symptoms():
    """Return list of available symptoms for frontend"""
    return jsonify({'symptoms': SYMPTOMS})

@diagnosis_bp.route('/', methods=['POST'])
def diagnose():
    data = request.get_json() or {}
    result = service.diagnose(data)
    return jsonify(result)

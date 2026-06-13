from flask import Blueprint, request, jsonify
from services.diagnosis_service import DiagnosisService
from ml.load_symptoms import SYMPTOMS

from flask import render_template

diagnosis_bp = Blueprint('diagnosis', __name__, url_prefix='/diagnosis')
service = DiagnosisService()


@diagnosis_bp.route('/symptoms', methods=['GET'])
def get_symptoms():
    """Return list of available symptoms for frontend"""
    return jsonify({'symptoms': SYMPTOMS})

@diagnosis_bp.route('/', methods=['POST'])
def diagnose():
    data = request.get_json() or {}
    result = service.diagnose(data)
    return jsonify(result)

from flask import Blueprint
from flask import request
from flask import jsonify

from services.chatbot_service import (
    ask_chatbot
)

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)

@chatbot_bp.route(
    "/ask",
    methods=["POST"]
)
def ask():

    data = request.get_json()

    question = data.get(
        "question"
    )

    answer = ask_chatbot(
        question
    )

    return jsonify({
        "answer": answer
    })
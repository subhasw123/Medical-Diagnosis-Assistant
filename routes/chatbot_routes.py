from flask import Blueprint, request, jsonify
from services.chatbot_service import ask_chatbot

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)

@chatbot_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")

    answer = ask_chatbot(
        question,
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent", "")[:255]
    )

    return jsonify({"answer": answer})
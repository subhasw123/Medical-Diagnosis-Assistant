from flask import Blueprint, request, jsonify
from services.chatbot_service import ask_chatbot

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)

@chatbot_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")

    try:
        answer = ask_chatbot(
            question,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent", "")[:255]
        )
        return jsonify({"answer": answer})
    except Exception as exc:
        print(f"[chatbot_error] {exc}")
        return jsonify({
            "answer": "Sorry, I couldn't connect to the AI service right now. Please try again in a moment."
        })

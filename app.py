from flask import Flask, render_template, request, session, redirect, url_for

from routes.diagnosis_routes import diagnosis_bp
from routes.chatbot_routes import chatbot_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)

app.secret_key = "medical_diagnosis_secret"

# Register blueprints
app.register_blueprint(diagnosis_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(chatbot_bp)


@app.route("/")
def home():
    # If an admin is logged in, redirect them to the admin dashboard
    # instead of showing the public user view
    if "admin" in session:
        return redirect(url_for("admin.dashboard"))

    return render_template("diagnosis.html", is_admin=False)


if __name__ == "__main__":
    app.run(debug=True)
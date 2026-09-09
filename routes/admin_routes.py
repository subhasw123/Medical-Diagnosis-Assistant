from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for
)
from functools import wraps

from database.admin_queries import (
    get_all_diagnoses,
    get_dashboard_stats
)
from ml.load_symptoms import SYMPTOMS

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ─── Auth Decorator ────────────────────────────────────────────────
def login_required(f):
    """Redirect to admin login if session is not authenticated."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function


# ─── Login / Logout ────────────────────────────────────────────────
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, go straight to dashboard
    if "admin" in session:
        return redirect(url_for("admin.dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):
            session["admin"] = username
            return redirect(url_for("admin.dashboard"))
        else:
            error = "Invalid username or password."

    return render_template("admin.html", error=error)


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


# ─── Dashboard ─────────────────────────────────────────────────────
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    diagnoses = get_all_diagnoses()
    stats = get_dashboard_stats()
    return render_template(
        "admin_dashboard.html",
        diagnoses=diagnoses,
        stats=stats
    )


# ─── Admin Diagnosis Tool ──────────────────────────────────────────
@admin_bp.route("/tool")
@login_required
def tool():
    """Admin view of the Diagnosis Tool — renders the same page
    but with is_admin=True so the template shows the admin navbar."""
    return render_template(
        "diagnosis.html",
        is_admin=True
    )


# ─── Admin AI Chatbot ──────────────────────────────────────────────
@admin_bp.route("/chatbot")
@login_required
def chatbot():
    """Admin view of the AI Chatbot section — scrolls directly to the
    chat section with the admin navbar visible."""
    return render_template(
        "diagnosis.html",
        is_admin=True,
        scroll_to_chat=True
    )
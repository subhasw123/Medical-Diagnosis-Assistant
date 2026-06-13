from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for
)

from database.admin_queries import (
    get_all_diagnoses,
    get_dashboard_stats
)

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin"] = username

            return redirect(
                url_for("admin.dashboard")
            )

    return render_template(
        "admin.html"
    )


@admin_bp.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(
            url_for("admin.login")
        )

    diagnoses = get_all_diagnoses()

    stats = get_dashboard_stats()

    return render_template(
        "admin_dashboard.html",
        diagnoses=diagnoses,
        stats=stats
    )

@admin_bp.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("admin.login")
    )
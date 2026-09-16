from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from mysql.connector import IntegrityError

from database.user_queries import authenticate_user, create_user, get_user_by_email
from database.diagnosis_queries import get_history
from utils.auth import user_login_required


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not all((full_name, email, age, gender, password, confirm_password)):
            flash("All fields are required.", "error")
        elif "@" not in email:
            flash("Enter a valid email address.", "error")
        elif not age.isdigit() or not 1 <= int(age) <= 120:
            flash("Age must be between 1 and 120.", "error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
        elif password != confirm_password:
            flash("Passwords do not match.", "error")
        elif get_user_by_email(email):
            flash("An account with that email already exists.", "error")
        else:
            try:
                user_id = create_user(full_name, email, int(age), gender, password)
            except IntegrityError:
                flash("An account with that email already exists.", "error")
            else:
                session.clear()
                session["user_id"] = user_id
                session["user_email"] = email
                return redirect(url_for("home"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = authenticate_user(email, password)

        if user:
            session.clear()
            session["user_id"] = user["user_id"]
            session["user_email"] = user["email"]
            next_url = request.args.get("next", "")
            if not next_url.startswith("/") or next_url.startswith("//"):
                next_url = url_for("home")
            return redirect(next_url)

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@auth_bp.route("/history")
@user_login_required
def history():
    return render_template(
        "history.html",
        rows=get_history(session["user_id"]),
        user_email=session.get("user_email"),
    )

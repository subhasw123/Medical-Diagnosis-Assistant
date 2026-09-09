from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    """
    Decorator that ensures the admin is logged in.
    Redirects to the admin login page if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function

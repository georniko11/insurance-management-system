from datetime import datetime, timezone
from urllib.parse import urlsplit
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.auth.services import authenticate_user
from app.models import User

def is_safe_next_url(target):
    if not target:
        return False

    if not target.startswith("/") or target.startswith("//"):
        return False

    if "\\" in target:
        return False

    parsed = urlsplit(target)

    return not parsed.scheme and not parsed.netloc

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user_data = authenticate_user(email, password)

        if user_data is None:
            flash("Λανθασμένο email ή κωδικός.", "danger")
            return render_template("auth/login.html")

        user = User(
            user_id=user_data["user_id"],
            name=user_data["name"],
            email=user_data["email"],
            is_active=user_data["is_active"]
        )

        login_user(user)
        session["last_activity"] = datetime.now(timezone.utc).timestamp()

        flash("Συνδέθηκες επιτυχώς!", "success")

        next_url = request.args.get("next")

        if is_safe_next_url(next_url):
            return redirect(next_url)

        return redirect(url_for("main.home"))

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    flash("Αποσυνδέθηκες επιτυχώς.", "success")
    return redirect(url_for("auth.login"))


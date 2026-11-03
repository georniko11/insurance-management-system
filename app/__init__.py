import math
from datetime import datetime, timezone

from flask import Flask, session, flash, redirect, url_for, request, render_template
from flask_login import LoginManager, current_user, logout_user
from flask_wtf.csrf import CSRFProtect, CSRFError

from config import Config

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Πρέπει να συνδεθείς για να συνεχίσεις."
login_manager.login_message_category = "warning"
@login_manager.user_loader
def load_user(user_id):
    from app.auth.queries import get_user_by_id
    from app.models import User

    user_data = get_user_by_id(user_id)

    if user_data is None or not user_data["is_active"]:
        return None

    return User(
        user_id=user_data["user_id"],
        name=user_data["name"],
        email=user_data["email"],
        is_active=user_data["is_active"]
    )

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    if not app.config.get("DATABASE_URL") or not app.config.get("SECRET_KEY"):
        raise RuntimeError("DATABASE_URL and SECRET_KEY must be set in .env")



    login_manager.init_app(app)

    from app import db
    db.init_app(app)

    from app.main import main
    app.register_blueprint(main)
    from app.customers import customers_bp
    app.register_blueprint(customers_bp)
    from app.policies import policies_bp
    app.register_blueprint(policies_bp)
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    csrf = CSRFProtect()
    csrf.init_app(app)
    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        app.logger.warning("CSRF validation failed: %s", error.description)

        return (
            render_template(
                "errors/csrf_error.html",
                message="Η φόρμα δεν είναι πλέον έγκυρη. "
                        "Ανανέωσε τη σελίδα και προσπάθησε ξανά."
            ),
            400
        )

    @app.before_request
    def check_idle_timeout():
        if not current_user.is_authenticated:
            return None

        if request.endpoint == "static":
            return None

        now = datetime.now(timezone.utc).timestamp()
        last_activity = session.get("last_activity")

        try:
            last_activity = float(last_activity)

            if not math.isfinite(last_activity):
                raise ValueError("Invalid last activity timestamp")

            elapsed = now - last_activity

            if elapsed < 0:
                elapsed = float("inf")

        except (TypeError, ValueError, OverflowError):
            elapsed = float("inf")

        if elapsed >= app.config["IDLE_TIMEOUT"].total_seconds():
            logout_user()
            session.pop("last_activity", None)

            flash(
                "Η σύνδεσή σου έληξε λόγω αδράνειας 30 λεπτών.",
                "warning"
            )
            return redirect(url_for("auth.login"))

        session["last_activity"] = now
        return None

    return app
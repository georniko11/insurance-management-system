from flask import Flask
from config import Config
from flask_wtf.csrf import CSRFProtect

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    if not app.config.get("DATABASE_URL") or not app.config.get("SECRET_KEY"):
        raise RuntimeError("DATABASE_URL and SECRET_KEY must be set in .env")


    from app import db
    db.init_app(app)

    from app.main import main
    app.register_blueprint(main)
    from app.customers import customers_bp
    app.register_blueprint(customers_bp)

    csrf = CSRFProtect()
    csrf.init_app(app)
    return app
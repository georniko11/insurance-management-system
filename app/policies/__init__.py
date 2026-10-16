from flask import Blueprint

policies_bp = Blueprint("policies", __name__)

from app.policies import routes
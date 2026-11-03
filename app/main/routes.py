from flask import render_template
from flask_login import login_required
from app.main import main


@main.route("/")
@login_required
def home():
    app_name = "Insurance Management System"

    return render_template("home.html", app_name=app_name)
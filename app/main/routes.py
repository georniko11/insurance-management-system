from flask import render_template
from app.main import main
from app.db import get_db

@main.route("/")
def home():
    app_name = "Insurance Management System"

    return render_template("home.html", app_name=app_name)



@main.route("/db-test")
def db_test():
    conn = get_db()
    cursor = conn.cursor()


    cursor.execute("SELECT COUNT(*) FROM customers")
    result = cursor.fetchone()
    customer_count = result["count"]


    return f"Customers in database: {customer_count}"
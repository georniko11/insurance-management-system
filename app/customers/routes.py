from psycopg.errors import UniqueViolation
from flask import render_template, abort, request, redirect, url_for

from app.customers import customers_bp
from app.customers.queries import (
    get_active_customers,
    get_customer_by_id,
    get_customer_phones,
    get_customer_emails,
    get_customer_by_afm,
    create_customer,
    update_customer,
    archive_customer,
    unarchive_customer
)


@customers_bp.route("/customers")
def list_customers():
    customers = get_active_customers()

    return render_template("customers.html", customers=customers)


@customers_bp.route("/customers/<int:customer_id>")
def customer_detail(customer_id):
    customer = get_customer_by_id(customer_id)

    if customer is None:
        abort(404)

    phones = get_customer_phones(customer_id)
    emails = get_customer_emails(customer_id)

    return render_template(
        "customer_detail.html",
        customer=customer,
        phones=phones,
        emails=emails
    )

@customers_bp.route("/customers/new", methods=["GET", "POST"])
def new_customer():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()

        afm = request.form.get("afm", "").strip() or None
        address = request.form.get("address", "").strip() or None
        notes = request.form.get("notes", "").strip() or None
        phone_number = request.form.get("phone_number", "").strip() or None

        if not first_name or not last_name:
            return "Το όνομα και το επώνυμο είναι υποχρεωτικά.", 400

        if afm is not None and (not afm.isdigit() or len(afm) != 9):
            return "Το ΑΦΜ πρέπει να αποτελείται από 9 ψηφία.", 400

        if afm is not None:
            existing_customer = get_customer_by_afm(afm)

            if existing_customer is not None:
                return "Υπάρχει ήδη πελάτης με αυτό το ΑΦΜ.", 409

        try:
            customer_id = create_customer(
                first_name,
                last_name,
                afm,
                address,
                notes,
                phone_number
            )
        except UniqueViolation:
            return "Υπάρχει ήδη καταχώρηση με αυτά τα μοναδικά στοιχεία.", 409

        return redirect(
            url_for(
                "customers.customer_detail",
                customer_id=customer_id
            )
        )

    return render_template("new_customer.html")

@customers_bp.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id):
    customer = get_customer_by_id(customer_id)

    if customer is None:
        abort(404)

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        afm = request.form.get("afm", "").strip() or None
        address = request.form.get("address", "").strip() or None
        notes = request.form.get("notes", "").strip() or None

        if not first_name or not last_name:
            return "Το όνομα και το επώνυμο είναι υποχρεωτικά.", 400

        if afm is not None and (not afm.isdigit() or len(afm) != 9):
            return "Το ΑΦΜ πρέπει να αποτελείται από 9 ψηφία.", 400

        if afm is not None:
            existing_customer = get_customer_by_afm(afm)

            if (
                existing_customer is not None
                and existing_customer["customer_id"] != customer_id
            ):
                return "Το ΑΦΜ ανήκει ήδη σε άλλον πελάτη.", 409

        try:
            updated_rows = update_customer(
                customer_id,
                first_name,
                last_name,
                afm,
                address,
                notes
            )
        except UniqueViolation:
            return "Το ΑΦΜ ανήκει ήδη σε άλλον πελάτη.", 409

        if updated_rows == 0:
            abort(404)

        return redirect(
            url_for(
                "customers.customer_detail",
                customer_id=customer_id
            )
        )

    return render_template("edit_customer.html", customer=customer)

@customers_bp.route("/customers/<int:customer_id>/archive", methods=["POST"])
def archive_customer_route(customer_id):
        customer = get_customer_by_id(customer_id)

        if customer is None:
           abort(404)

        if customer["is_archived"]:
           return "Ο πελάτης είναι ήδη αρχειοθετημένος.", 409

        archive_customer(customer_id)

        return redirect(url_for("customers.list_customers"))

@customers_bp.route("/customers/<int:customer_id>/unarchive", methods=["POST"])
def unarchive_customer_route(customer_id):
    customer = get_customer_by_id(customer_id)

    if customer is None:
        abort(404)

    if not customer["is_archived"]:
        return "Ο πελάτης είναι ήδη ενεργός.", 409

    updated_rows = unarchive_customer(customer_id)

    if updated_rows == 0:
        return "Δεν ήταν δυνατή η επαναφορά.", 409

    return redirect(
        url_for("customers.customer_detail", customer_id=customer_id)
    )
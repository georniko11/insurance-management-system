import re
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
    unarchive_customer,
    get_customers_by_status,
    count_active_policies,
    count_pending_renewals,
)



@customers_bp.route("/customers")
def list_customers():
    status = request.args.get("status", "active")

    if status not in ("active", "archived", "all"):
        abort(400)

    customers = get_customers_by_status(status)

    return render_template(
        "customers.html",
        customers=customers,
        status=status
    )




@customers_bp.route("/customers/<int:customer_id>")
def customer_detail(customer_id):
    customer = get_customer_by_id(customer_id)

    if customer is None:
        abort(404)

    phones = get_customer_phones(customer_id)
    emails = get_customer_emails(customer_id)
    active_count = count_active_policies(customer_id)

    return render_template(
        "customer_detail.html",
        customer=customer,
        phones=phones,
        emails=emails,
        active_count=active_count
    )


@customers_bp.route("/customers/new", methods=["GET", "POST"])
def new_customer():
    if request.method == "GET":
        return render_template(
            "new_customer.html",
            form_data={},
            error=None
        )

    # Διαβάζουμε τα δεδομένα της φόρμας
    form_data = request.form.to_dict()

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    afm = request.form.get("afm", "").strip() or None
    address = request.form.get("address", "").strip() or None
    notes = request.form.get("notes", "").strip() or None

    phone_input = request.form.get("phone_number", "").strip()

    # Αφαιρούμε κενά και παύλες από το τηλέφωνο
    phone_number = re.sub(r"[\s-]", "", phone_input)

    def form_error(message, status=400):
        return render_template(
            "new_customer.html",
            form_data=form_data,
            error=message
        ), status

    # Υποχρεωτικά πεδία
    if not first_name or not last_name:
        return form_error("Το όνομα και το επώνυμο είναι υποχρεωτικά.")

    if not phone_number:
        return form_error("Το τηλέφωνο είναι υποχρεωτικό.")

    # Μέγιστα μήκη
    if len(first_name) > 50:
        return form_error("Το όνομα δεν μπορεί να ξεπερνά τους 50 χαρακτήρες.")

    if len(last_name) > 50:
        return form_error("Το επώνυμο δεν μπορεί να ξεπερνά τους 50 χαρακτήρες.")

    if address is not None and len(address) > 200:
        return form_error("Η διεύθυνση δεν μπορεί να ξεπερνά τους 200 χαρακτήρες.")

    # Έλεγχος ΑΦΜ
    if afm is not None and not re.fullmatch(r"[0-9]{9}", afm):
        return form_error("Το ΑΦΜ πρέπει να αποτελείται από 9 ψηφία.")

    # Έλεγχος τηλεφώνου
    if not re.fullmatch(r"\+?[0-9]{7,15}", phone_number):
        return form_error(
            "Το τηλέφωνο πρέπει να έχει 7–15 ψηφία και προαιρετικά + στην αρχή."
        )

    # Έλεγχος διπλού ΑΦΜ
    if afm is not None:
        existing_customer = get_customer_by_afm(afm)

        if existing_customer is not None:
            return form_error("Υπάρχει ήδη πελάτης με αυτό το ΑΦΜ.", 409)

    # Αποθήκευση στη βάση
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
        return form_error(
            "Υπάρχει ήδη καταχώρηση με αυτά τα μοναδικά στοιχεία.",
            409
        )

    return redirect(
        url_for(
            "customers.customer_detail",
            customer_id=customer_id
        )
    )




@customers_bp.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def edit_customer(customer_id):
    customer = get_customer_by_id(customer_id)

    if customer is None:
        abort(404)

    # Δεν επιτρέπουμε επεξεργασία αρχειοθετημένων πελατών
    if customer["is_archived"]:
        abort(403)

    if request.method == "GET":
        return render_template(
            "edit_customer.html",
            customer=customer,
            form_data={
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "afm": customer["afm"] or "",
                "address": customer["address"] or "",
                "notes": customer["notes"] or ""
            },
            error=None
        )

    form_data = request.form.to_dict()

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    afm = request.form.get("afm", "").strip() or None
    address = request.form.get("address", "").strip() or None
    notes = request.form.get("notes", "").strip() or None

    def form_error(message, status=400):
        return render_template(
            "edit_customer.html",
            customer=customer,
            form_data=form_data,
            error=message
        ), status

    if not first_name or not last_name:
        return form_error("Το όνομα και το επώνυμο είναι υποχρεωτικά.")

    if len(first_name) > 50:
        return form_error("Το όνομα δεν μπορεί να ξεπερνά τους 50 χαρακτήρες.")

    if len(last_name) > 50:
        return form_error("Το επώνυμο δεν μπορεί να ξεπερνά τους 50 χαρακτήρες.")

    if address is not None and len(address) > 200:
        return form_error("Η διεύθυνση δεν μπορεί να ξεπερνά τους 200 χαρακτήρες.")

    if afm is not None and not re.fullmatch(r"[0-9]{9}", afm):
        return form_error("Το ΑΦΜ πρέπει να αποτελείται από 9 ψηφία.")

    if afm is not None:
        existing_customer = get_customer_by_afm(afm)

        if (
            existing_customer is not None
            and existing_customer["customer_id"] != customer_id
        ):
            return form_error("Το ΑΦΜ ανήκει ήδη σε άλλον πελάτη.", 409)

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
        return form_error("Το ΑΦΜ ανήκει ήδη σε άλλον πελάτη.", 409)

    if updated_rows == 0:
        abort(404)

    return redirect(
        url_for(
            "customers.customer_detail",
            customer_id=customer_id
        )
    )

@customers_bp.route("/customers/<int:customer_id>/archive", methods=["POST"])
def archive_customer_route(customer_id):
    customer = get_customer_by_id(customer_id)

    if customer is None:
        abort(404)

    if customer["is_archived"]:
        return "Ο πελάτης είναι ήδη αρχειοθετημένος.", 409

    active_count = count_active_policies(customer_id)
    pending_count = count_pending_renewals(customer_id)

    if (active_count > 0 or pending_count > 0) and request.form.get("confirm_archive") != "yes":

        phones = get_customer_phones(customer_id)
        emails = get_customer_emails(customer_id)

        return render_template(
            "customer_detail.html",
            customer=customer,
            phones=phones,
            emails=emails,
            active_count=active_count,
            pending_count=pending_count,
            archive_warning=True
        )

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
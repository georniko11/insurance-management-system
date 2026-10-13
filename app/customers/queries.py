from app.db import get_db


def get_active_customers():
    conn = get_db()

    cursor = conn.execute("""
        SELECT customer_id, first_name, last_name, afm
        FROM customers
        WHERE is_archived = false
        ORDER BY last_name, first_name
    """)

    return cursor.fetchall()

def get_customer_by_id(customer_id):
    conn = get_db()

    customer = conn.execute("""
        SELECT customer_id, first_name, last_name,
               afm, address, notes, is_archived
        FROM customers
        WHERE customer_id = %s
    """, (customer_id,)).fetchone()

    return customer

def get_customer_phones(customer_id):
    conn = get_db()

    phones = conn.execute("""
        SELECT phone_id, phone_number, is_primary
        FROM customer_phones
        WHERE customer_id = %s
        ORDER BY is_primary DESC, phone_id
    """, (customer_id,)).fetchall()

    return phones

def get_customer_emails(customer_id):
    conn = get_db()

    emails = conn.execute("""
        SELECT email_id, email_address, is_primary
        FROM customer_emails
        WHERE customer_id = %s
        ORDER BY is_primary DESC, email_id
    """, (customer_id,)).fetchall()

    return emails

def create_customer(first_name, last_name, afm, address, notes, phone_number):
    conn = get_db()

    with conn.transaction():
        customer = conn.execute("""
            INSERT INTO customers (
                first_name, last_name, afm, address, notes
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING customer_id
        """, (
            first_name, last_name, afm, address, notes
        )).fetchone()

        customer_id = customer["customer_id"]

        if phone_number:
            conn.execute("""
                INSERT INTO customer_phones (
                    customer_id, phone_number, is_primary
                )
                VALUES (%s, %s, %s)
            """, (customer_id, phone_number, True))

    return customer_id

def get_customer_by_afm(afm):
    conn = get_db()

    customer = conn.execute("""
        SELECT customer_id, first_name, last_name
        FROM customers
        WHERE afm = %s
    """, (afm,)).fetchone()

    return customer

def update_customer(customer_id, first_name, last_name, afm, address, notes):
    conn = get_db()

    with conn.transaction():
        result = conn.execute("""
            UPDATE customers
            SET
                first_name = %s,
                last_name = %s,
                afm = %s,
                address = %s,
                notes = %s
            WHERE customer_id = %s
        """, (
            first_name,
            last_name,
            afm,
            address,
            notes,
            customer_id
        ))

    return result.rowcount

def archive_customer(customer_id):
    conn = get_db()

    with conn.transaction():
        result = conn.execute("""
            UPDATE customers
            SET
                is_archived = true,
                archived_at = CURRENT_TIMESTAMP
            WHERE customer_id = %s
              AND is_archived = false
        """, (customer_id,))

    return result.rowcount

def unarchive_customer(customer_id):
    conn = get_db()

    with conn.transaction():
        result = conn.execute("""
            UPDATE customers
            SET
                is_archived = false,
                archived_at = NULL
            WHERE customer_id = %s
              AND is_archived = true
        """, (customer_id,))

    return result.rowcount
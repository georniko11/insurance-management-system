from app.db import get_db
POLICY_STATUS_SQL = """
    CASE
        WHEN p.cancellation_date IS NOT NULL
            THEN 'cancelled'

        WHEN p.end_date < CURRENT_DATE
             AND EXISTS (
                 SELECT 1
                 FROM policies AS next_p
                 WHERE next_p.previous_policy_id = p.policy_id
             )
            THEN 'renewed'

        WHEN p.end_date < CURRENT_DATE
            THEN 'expired'

        WHEN p.start_date > CURRENT_DATE
            THEN 'future'

        ELSE 'active'
    END
"""


# ==========================================
# 1. Λίστα όλων των ασφαλιστηρίων
# ==========================================

def get_all_policies():
    db = get_db()

    policies = db.execute(f"""
        SELECT
            p.policy_id,
            p.policy_number,
            p.policy_type,
            p.start_date,
            p.end_date,
            p.premium,
            c.first_name,
            c.last_name,
            i.name AS insurer_name,

           {POLICY_STATUS_SQL} AS status

        FROM policies AS p

        JOIN customers AS c
            ON p.customer_id = c.customer_id

        JOIN insurers AS i
            ON p.insurer_id = i.insurer_id

        ORDER BY p.end_date
    """).fetchall()

    return policies


# ==========================================
# 2. Λεπτομέρειες συγκεκριμένου ασφαλιστηρίου
# ==========================================

def get_policy_by_id(policy_id):
    db = get_db()

    policy = db.execute(f"""
        SELECT
            p.*,
            c.first_name,
            c.last_name,
            i.name AS insurer_name,

         {POLICY_STATUS_SQL} AS status

        FROM policies AS p

        JOIN customers AS c
            ON p.customer_id = c.customer_id

        JOIN insurers AS i
            ON p.insurer_id = i.insurer_id

        WHERE p.policy_id = %s
    """, (policy_id,)).fetchone()

    return policy


# ==========================================
# 3. Στοιχεία ασφαλιστηρίου οχήματος
# ==========================================

def get_motor_policy_details(policy_id):
    db = get_db()

    details = db.execute("""
        SELECT
            v.plate,
            v.make,
            v.model,
            v.vehicle_type,
            mpd.coverage_category,
            mpd.package_name

        FROM motor_policy_details AS mpd

        JOIN vehicles AS v
            ON mpd.vehicle_id = v.vehicle_id

        WHERE mpd.policy_id = %s
    """, (policy_id,)).fetchone()

    return details


# ==========================================
# 4. Στοιχεία ασφαλιστηρίου κατοικίας
# ==========================================

def get_home_policy_details(policy_id):
    db = get_db()

    details = db.execute("""
        SELECT
            pr.address,
            pr.property_type,
            pr.square_meters,
            hpd.building_coverage_amount,
            hpd.contents_coverage_amount,
            hpd.fire_theft_coverage

        FROM home_policy_details AS hpd

        JOIN properties AS pr
            ON hpd.property_id = pr.property_id

        WHERE hpd.policy_id = %s
    """, (policy_id,)).fetchone()

    return details


# ==========================================
# 5. Στοιχεία ασφαλιστηρίου υγείας
# ==========================================

def get_health_policy_details(policy_id):
    db = get_db()

    details = db.execute("""
        SELECT
            plan_type,
            plan_name

        FROM health_policy_details

        WHERE policy_id = %s
    """, (policy_id,)).fetchone()

    return details

def get_next_policy(policy_id):
    db = get_db()

    next_policy = db.execute("""
        SELECT
            policy_id,
            policy_number,
            start_date,
            end_date
        FROM policies
        WHERE previous_policy_id = %s
    """, (policy_id,)).fetchone()

    return next_policy

def get_previous_policy(policy_id):
    db = get_db()

    previous_policy = db.execute("""
        SELECT
            previous_p.policy_id,
            previous_p.policy_number,
            previous_p.start_date,
            previous_p.end_date
        FROM policies AS p
        JOIN policies AS previous_p
            ON p.previous_policy_id = previous_p.policy_id
        WHERE p.policy_id = %s
    """, (policy_id,)).fetchone()

    return previous_policy
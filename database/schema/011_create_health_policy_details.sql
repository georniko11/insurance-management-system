CREATE TABLE health_policy_details (
    policy_id INTEGER PRIMARY KEY,

    customer_id INTEGER NOT NULL,

    policy_type VARCHAR(20) NOT NULL DEFAULT 'health'
        CHECK (policy_type = 'health'),

    plan_type VARCHAR(20) NOT NULL
        CHECK (
            plan_type IN ('individual', 'family')
        ),

    plan_name VARCHAR(100),

    FOREIGN KEY (policy_id, customer_id, policy_type)
        REFERENCES policies(policy_id, customer_id, policy_type),

    CHECK (
        plan_name IS NULL
        OR btrim(plan_name) <> ''
    )
);
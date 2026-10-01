CREATE TABLE policies (
    policy_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_id INTEGER NOT NULL
        REFERENCES customers(customer_id),

    insurer_id INTEGER NOT NULL
        REFERENCES insurers(insurer_id),

    policy_number VARCHAR(50) NOT NULL,

    policy_type VARCHAR(20) NOT NULL
        CHECK (
            policy_type IN ('motor', 'home', 'health')
        ),

    start_date DATE NOT NULL,

    end_date DATE NOT NULL,

    premium NUMERIC(10,2) NOT NULL
        CHECK (premium > 0),

    cancellation_date DATE,

    cancellation_reason VARCHAR(30)
        CHECK (
            cancellation_reason IN (
                'sale',
                'plate_surrender',
                'customer_request',
                'insurer_cancelled',
                'unpaid_premium',
                'replaced',
                'other'
            )
        ),

    cancellation_notes TEXT,

    previous_policy_id INTEGER,

    created_by INTEGER NOT NULL
        REFERENCES users(user_id),

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (insurer_id, policy_number),

    UNIQUE (previous_policy_id),

    UNIQUE (policy_id, customer_id, policy_type),

    FOREIGN KEY (previous_policy_id, customer_id, policy_type)
        REFERENCES policies(policy_id, customer_id, policy_type),

    CHECK (
        btrim(policy_number) <> ''
    ),

    CHECK (
        policy_number = btrim(policy_number)
    ),

    CHECK (
        end_date > start_date
    ),

    CHECK (
        (cancellation_date IS NULL AND cancellation_reason IS NULL)
        OR
        (cancellation_date IS NOT NULL AND cancellation_reason IS NOT NULL)
    ),

    CHECK (
        cancellation_date IS NULL
        OR cancellation_date >= start_date
    ),

    CHECK (
        cancellation_date IS NULL
        OR cancellation_date < end_date
    ),

    CHECK (
        cancellation_notes IS NULL
        OR cancellation_date IS NOT NULL
    ),

    CHECK (
        previous_policy_id IS NULL
        OR previous_policy_id <> policy_id
    )
);

CREATE INDEX idx_policies_customer_id
ON policies(customer_id);

CREATE INDEX idx_policies_end_date
ON policies(end_date);
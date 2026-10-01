CREATE TABLE renewals (
    renewal_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    policy_id INTEGER NOT NULL UNIQUE
        REFERENCES policies(policy_id),

    status VARCHAR(30) NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'contacted',
                'customer_wants_renewal',
                'awaiting_payment',
                'paid',
                'renewed',
                'no_response',
                'lost'
            )
        ),

    follow_up_date DATE,

    assigned_to INTEGER NOT NULL
        REFERENCES users(user_id),

    paid_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    status_updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CHECK (
        (status IN ('paid', 'renewed') AND paid_at IS NOT NULL)
        OR
        (status NOT IN ('paid', 'renewed') AND paid_at IS NULL)
    ),

    CHECK (
        follow_up_date IS NULL
        OR status NOT IN ('renewed', 'lost')
    )
);

CREATE INDEX idx_renewals_assigned_to
ON renewals(assigned_to);

CREATE INDEX idx_renewals_follow_up_date
ON renewals(follow_up_date);
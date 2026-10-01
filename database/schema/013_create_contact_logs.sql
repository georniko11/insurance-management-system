CREATE TABLE contact_logs (
    contact_log_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    renewal_id INTEGER NOT NULL
        REFERENCES renewals(renewal_id),

    user_id INTEGER NOT NULL
        REFERENCES users(user_id),

    contact_type VARCHAR(20) NOT NULL
        CHECK (
            contact_type IN (
                'telephone',
                'message',
                'email'
            )
        ),

    outcome VARCHAR(30) NOT NULL
        CHECK (
            outcome IN (
                'no_answer',
                'reached',
                'message_sent',
                'callback_requested',
                'wants_renewal',
                'does_not_want_renewal'
            )
        ),

    notes TEXT,

    contacted_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CHECK (
        notes IS NULL
        OR btrim(notes) <> ''
    ),

    CHECK (
        outcome <> 'message_sent'
        OR contact_type IN ('message', 'email')
    ),

    CHECK (
        outcome <> 'no_answer'
        OR contact_type = 'telephone'
    )
);

CREATE INDEX idx_contact_logs_renewal_contacted
ON contact_logs(renewal_id, contacted_at DESC);

CREATE INDEX idx_contact_logs_user_id
ON contact_logs(user_id);
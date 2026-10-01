CREATE TABLE activity_log (
    activity_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id),

    action VARCHAR(30) NOT NULL
        CHECK (
            action IN (
                'create',
                'update',
                'status_change',
                'cancel',
                'archive',
                'reactivate',
                'reassign',
                'deactivate'
            )
        ),

    entity_type VARCHAR(30) NOT NULL
        CHECK (
            entity_type IN (
                'customer',
                'policy',
                'renewal',
                'contact_log',
                'vehicle',
                'property',
                'insurer',
                'user'
            )
        ),

    entity_id INTEGER NOT NULL,

    details JSONB,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CHECK (
        details IS NULL
        OR jsonb_typeof(details) = 'object'
    ),

    CHECK (
        action NOT IN (
            'update',
            'status_change',
            'cancel',
            'reassign'
        )
        OR details IS NOT NULL
    )
);

CREATE INDEX idx_activity_log_entity
ON activity_log(entity_type, entity_id, created_at DESC);

CREATE INDEX idx_activity_log_user_id
ON activity_log(user_id);
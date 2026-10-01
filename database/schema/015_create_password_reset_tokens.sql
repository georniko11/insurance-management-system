CREATE TABLE password_reset_tokens (
    reset_token_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id INTEGER NOT NULL
        REFERENCES users(user_id),

    token_hash CHAR(64) NOT NULL UNIQUE
        CHECK (token_hash ~ '^[0-9a-f]{64}$'),

    expires_at TIMESTAMPTZ NOT NULL,

    used_at TIMESTAMPTZ,

    revoked_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CHECK (
        expires_at > created_at
    ),

    CHECK (
        used_at IS NULL
        OR used_at >= created_at
    ),

    CHECK (
        used_at IS NULL
        OR used_at <= expires_at
    ),

    CHECK (
        revoked_at IS NULL
        OR revoked_at >= created_at
    ),

    CHECK (
        used_at IS NULL
        OR revoked_at IS NULL
    )
);

CREATE INDEX idx_password_reset_tokens_user_id
ON password_reset_tokens(user_id);
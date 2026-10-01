CREATE TABLE users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(255) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    is_demo BOOLEAN NOT NULL DEFAULT FALSE,

    deactivated_at TIMESTAMPTZ,

    last_login_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CHECK (
        btrim(name) <> ''
    ),

    CHECK (
        btrim(email) <> ''
    ),

    CHECK (
        email = lower(email)
    ),

    CHECK (
        (is_active = TRUE AND deactivated_at IS NULL)
        OR
        (is_active = FALSE AND deactivated_at IS NOT NULL)
    )
);
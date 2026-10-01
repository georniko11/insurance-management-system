CREATE TABLE customers (
    customer_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,

    afm VARCHAR(9) UNIQUE,

    address VARCHAR(200),
    notes TEXT,

    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    archived_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (btrim(first_name) <> ''),
    CHECK (btrim(last_name) <> ''),

    CHECK (
        afm IS NULL
        OR afm ~ '^[0-9]{9}$'
    ),

    CHECK (
        (is_archived = FALSE AND archived_at IS NULL)
        OR
        (is_archived = TRUE AND archived_at IS NOT NULL)
    )
);
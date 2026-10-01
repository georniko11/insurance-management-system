CREATE TABLE insurers (
    insurer_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CHECK (btrim(name) <> ''),

    CHECK (name = btrim(name))
);

CREATE UNIQUE INDEX unique_insurer_name_ci
ON insurers (lower(name));
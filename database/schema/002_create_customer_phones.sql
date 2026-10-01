CREATE TABLE customer_phones (
    phone_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_id INTEGER NOT NULL
        REFERENCES customers(customer_id),

    phone_number VARCHAR(20) NOT NULL,

    is_primary BOOLEAN NOT NULL DEFAULT FALSE,

    UNIQUE (customer_id, phone_number),

    CHECK (btrim(phone_number) <> ''),

    CHECK (
        phone_number ~ '^\+?[0-9]{7,15}$'
    )
);

CREATE UNIQUE INDEX unique_primary_phone_per_customer
ON customer_phones(customer_id)
WHERE is_primary = TRUE;
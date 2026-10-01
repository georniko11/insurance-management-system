CREATE TABLE customer_emails (
    email_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_id INTEGER NOT NULL
        REFERENCES customers(customer_id),

    email_address VARCHAR(255) NOT NULL,

    is_primary BOOLEAN NOT NULL DEFAULT FALSE,

    UNIQUE (customer_id, email_address),

    CHECK (btrim(email_address) <> ''),

    CHECK (
        email_address = lower(email_address)
    )
);

CREATE UNIQUE INDEX unique_primary_email_per_customer
ON customer_emails(customer_id)
WHERE is_primary = TRUE;
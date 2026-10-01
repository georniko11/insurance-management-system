CREATE TABLE properties (
    property_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_id INTEGER NOT NULL
        REFERENCES customers(customer_id),

    address VARCHAR(200) NOT NULL,

    property_type VARCHAR(20) NOT NULL
        CHECK (
            property_type IN (
                'apartment',
                'house',
                'commercial',
                'other'
            )
        ),

    square_meters NUMERIC(8,2),

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (property_id, customer_id),

    CHECK (
        btrim(address) <> ''
    ),

    CHECK (
        square_meters IS NULL
        OR square_meters > 0
    )
);

CREATE INDEX idx_properties_customer_id
ON properties(customer_id);
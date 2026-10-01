CREATE TABLE vehicles (
    vehicle_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_id INTEGER NOT NULL
        REFERENCES customers(customer_id),

    plate VARCHAR(15) NOT NULL,

    plate_normalized VARCHAR(15) GENERATED ALWAYS AS (
        translate(
            upper(regexp_replace(plate, '[^[:alnum:]]', '', 'g')),
            'ΑΒΕΖΗΙΚΜΝΟΡΤΥΧ',
            'ABEZHIKMNOPTYX'
        )
    ) STORED UNIQUE,

    vehicle_type VARCHAR(20) NOT NULL
        CHECK (
            vehicle_type IN (
                'car',
                'motorcycle',
                'truck',
                'other'
            )
        ),

    make VARCHAR(50),

    model VARCHAR(50),

    registration_date DATE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (vehicle_id, customer_id),

    CHECK (
        plate_normalized ~ '^[A-Z0-9]{2,12}$'
    ),

    CHECK (
        make IS NULL
        OR btrim(make) <> ''
    ),

    CHECK (
        model IS NULL
        OR btrim(model) <> ''
    )
);

CREATE INDEX idx_vehicles_customer_id
ON vehicles(customer_id);
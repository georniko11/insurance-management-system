CREATE TABLE motor_policy_details (
    policy_id INTEGER PRIMARY KEY,

    customer_id INTEGER NOT NULL,

    policy_type VARCHAR(20) NOT NULL DEFAULT 'motor'
        CHECK (policy_type = 'motor'),

    vehicle_id INTEGER NOT NULL,

    coverage_category VARCHAR(20) NOT NULL
        CHECK (
            coverage_category IN (
                'basic',
                'fire_theft',
                'comprehensive'
            )
        ),

    package_name VARCHAR(100),

    FOREIGN KEY (policy_id, customer_id, policy_type)
        REFERENCES policies(policy_id, customer_id, policy_type),

    FOREIGN KEY (vehicle_id, customer_id)
        REFERENCES vehicles(vehicle_id, customer_id),

    CHECK (
        package_name IS NULL
        OR btrim(package_name) <> ''
    )
);

CREATE INDEX idx_motor_policy_details_vehicle_id
ON motor_policy_details(vehicle_id);
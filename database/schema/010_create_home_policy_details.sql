CREATE TABLE home_policy_details (
    policy_id INTEGER PRIMARY KEY,

    customer_id INTEGER NOT NULL,

    policy_type VARCHAR(20) NOT NULL DEFAULT 'home'
        CHECK (policy_type = 'home'),

    property_id INTEGER NOT NULL,

    building_coverage_amount NUMERIC(12,2),

    contents_coverage_amount NUMERIC(12,2),

    fire_theft_coverage BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (policy_id, customer_id, policy_type)
        REFERENCES policies(policy_id, customer_id, policy_type),

    FOREIGN KEY (property_id, customer_id)
        REFERENCES properties(property_id, customer_id),

    CHECK (
        building_coverage_amount IS NULL
        OR building_coverage_amount > 0
    ),

    CHECK (
        contents_coverage_amount IS NULL
        OR contents_coverage_amount > 0
    )
);

CREATE INDEX idx_home_policy_details_property_id
ON home_policy_details(property_id);
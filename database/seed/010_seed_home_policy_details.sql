INSERT INTO home_policy_details (
    policy_id,
    customer_id,
    property_id,
    building_coverage_amount,
    contents_coverage_amount,
    fire_theft_coverage
)
VALUES
    (11, 1,  1,  120000.00, 20000.00, TRUE),
    (12, 4,  3,  95000.00,  15000.00, TRUE),
    (13, 6,  4,  180000.00, 30000.00, TRUE),
    (14, 10, 6,  210000.00, 40000.00, FALSE),
    (15, 14, 8,  165000.00, 25000.00, TRUE),
    (16, 18, 10, 110000.00, 18000.00, FALSE);
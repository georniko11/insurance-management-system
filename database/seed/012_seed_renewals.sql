INSERT INTO renewals (
    policy_id,
    status,
    follow_up_date,
    assigned_to
)
VALUES
    (3,  'no_response',                '2026-10-05', 1),
    (4,  'contacted',              '2026-10-08', 2),
    (8,  'lost',                   NULL,         3),
    (12, 'customer_wants_renewal', '2026-10-07', 2),
    (15, 'awaiting_payment',       '2026-10-09', 1);
    INSERT INTO renewals (
    policy_id,
    status,
    follow_up_date,
    assigned_to,
    paid_at
)
VALUES
    (18, 'paid', '2026-10-06', 2, '2026-10-04 11:00:00+03');
    INSERT INTO renewals (
    policy_id,
    status,
    follow_up_date,
    assigned_to,
    paid_at
)
VALUES
    (6, 'renewed', NULL, 1, '2026-10-02 10:15:00+03');
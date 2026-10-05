INSERT INTO activity_log (
    user_id,
    action,
    entity_type,
    entity_id,
    details
)
VALUES
        (1, 'create', 'policy', 1, NULL),

    (2, 'status_change', 'renewal', 2,
     '{"old_status": "pending", "new_status": "contacted"}'),

    (2, 'status_change', 'renewal', 4,
     '{"old_status": "contacted", "new_status": "customer_wants_renewal"}'),

    (1, 'reassign', 'renewal', 5,
     '{"old_assigned_to": 2, "new_assigned_to": 1}'),

    (3, 'update', 'customer', 8,
     '{"field": "address", "reason": "customer_update"}');
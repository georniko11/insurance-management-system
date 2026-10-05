INSERT INTO contact_logs (
    renewal_id,
    user_id,
    contact_type,
    outcome,
    notes
)
VALUES
        (1, 1, 'telephone', 'no_answer',
     'Δεν απάντησε στην κλήση'),

    (2, 2, 'telephone', 'reached',
     'Έγινε επικοινωνία με τον πελάτη'),

    (3, 3, 'telephone', 'does_not_want_renewal',
     'Ο πελάτης δεν επιθυμεί ανανέωση'),

    (4, 2, 'telephone', 'wants_renewal',
     'Ο πελάτης επιθυμεί να προχωρήσει σε ανανέωση'),

    (5, 1, 'message', 'message_sent',
     'Στάλθηκε μήνυμα υπενθύμισης πληρωμής'),

    (6, 2, 'email', 'message_sent',
     'Στάλθηκε email σχετικά με την πληρωμή'),

    (7, 1, 'telephone', 'wants_renewal',
     'Η ανανέωση ολοκληρώθηκε μετά από επικοινωνία');
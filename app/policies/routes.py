from flask import render_template, abort

from app.policies import policies_bp
from app.policies.queries import (
    get_all_policies,
    get_policy_by_id,
    get_motor_policy_details,
    get_home_policy_details,
    get_health_policy_details,
    get_next_policy,
    get_previous_policy
)


@policies_bp.route("/policies")
def list_policies():
    policies = get_all_policies()
    return render_template("policies/list.html", policies=policies)

@policies_bp.route("/policies/<int:policy_id>")
def policy_detail(policy_id):
    policy = get_policy_by_id(policy_id)

    if policy is None:
        abort(404)

    next_policy = get_next_policy(policy_id)

    previous_policy = get_previous_policy(policy_id)

    motor_details = None
    home_details = None
    health_details = None

    if policy["policy_type"] == "motor":
        motor_details = get_motor_policy_details(policy_id)

    elif policy["policy_type"] == "home":
        home_details = get_home_policy_details(policy_id)

    elif policy["policy_type"] == "health":
        health_details = get_health_policy_details(policy_id)

    return render_template(
    "policies/detail.html",
    policy=policy,
    motor_details=motor_details,
    home_details=home_details,
    health_details=health_details,
    next_policy=next_policy,
    previous_policy=previous_policy
)
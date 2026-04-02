"""
Remediator: matches an alert to a runbook and simulates execution.
"""
from runbooks import registry


def attempt_remediation(alert: dict, classification: dict) -> dict:
    severity = classification["severity"]
    category = classification["category"]

    runbook = registry.find_runbook(severity, category, alert)
    if not runbook:
        return {
            "status": "skipped",
            "action": "No matching runbook found",
            "runbook_id": None,
        }

    result = runbook.execute(alert)
    return {
        "status": result["status"],
        "action": result["action"],
        "runbook_id": runbook.id,
    }

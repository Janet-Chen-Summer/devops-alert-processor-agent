"""
Router: decides which mock channels receive an alert and
calls each notifier with the alert payload.
"""
from notifiers.slack import send_slack
from notifiers.pagerduty import send_pagerduty
from notifiers.email import send_email

# Routing matrix: (severity, category) → list of notifiers to invoke
ROUTING_TABLE = {
    ("critical", "infra"):       ["pagerduty", "slack", "email"],
    ("critical", "app"):         ["pagerduty", "slack"],
    ("critical", "security"):    ["pagerduty", "slack", "email"],
    ("critical", "performance"): ["pagerduty", "slack"],
    ("high", "infra"):           ["slack", "email"],
    ("high", "app"):             ["slack"],
    ("high", "security"):        ["slack", "email"],
    ("high", "performance"):     ["slack"],
    ("medium", "infra"):         ["slack"],
    ("medium", "app"):           ["slack"],
    ("medium", "security"):      ["slack", "email"],
    ("medium", "performance"):   ["slack"],
    ("low", "infra"):            [],
    ("low", "app"):              [],
    ("low", "security"):         ["email"],
    ("low", "performance"):      [],
}

NOTIFIER_FNS = {
    "slack": send_slack,
    "pagerduty": send_pagerduty,
    "email": send_email,
}


def route_alert(classification: dict) -> list[str]:
    key = (classification["severity"], classification["category"])
    destinations = ROUTING_TABLE.get(key, ["slack"])

    for dest in destinations:
        fn = NOTIFIER_FNS.get(dest)
        if fn:
            fn(classification)

    return destinations

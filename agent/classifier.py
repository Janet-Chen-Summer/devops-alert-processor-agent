"""
Classifier: assigns severity (critical/high/medium/low) and
category (infra/app/security/performance) to an incoming alert.
"""

SEVERITY_RULES = [
    {"keywords": ["error", "down", "outage", "unreachable", "fatal", "crash", "oom killed"], "severity": "critical"},
    {"keywords": ["disk full", "memory", "5xx", "cpu spike", "brute", "brute-force", "cert"], "severity": "high"},
    {"keywords": ["warning", "slow", "degraded", "retry", "timeout", "latency"], "severity": "medium"},
    {"keywords": ["info", "notice", "scaling", "deploy", "restart"], "severity": "low"},
]

CATEGORY_RULES = [
    {"keywords": ["cpu", "memory", "disk", "node", "host", "oom", "kernel"], "category": "infra"},
    {"keywords": ["pod", "container", "deploy", "endpoint", "5xx", "error rate"], "category": "app"},
    {"keywords": ["auth", "login", "brute", "brute-force", "injection", "firewall", "certificate", "tls", "cert"], "category": "security"},
    {"keywords": ["latency", "throughput", "slow", "p99", "queue depth", "apdex"], "category": "performance"},
]

ACTION_MAP = {
    ("critical", "infra"): "Page on-call SRE immediately and initiate incident bridge",
    ("critical", "app"): "Rollback last deployment and open incident ticket",
    ("critical", "security"): "Isolate affected resource and notify security team",
    ("critical", "performance"): "Enable traffic shedding and scale horizontally",
    ("high", "infra"): "Investigate resource utilisation; check runbook RB-INFRA-01",
    ("high", "app"): "Review recent deploys and error traces in APM",
    ("high", "security"): "Audit auth logs and temporarily block suspicious IPs",
    ("high", "performance"): "Profile hot paths; check DB query plans",
    ("medium", "infra"): "Monitor trend; schedule maintenance if persists",
    ("medium", "app"): "Review logs; create Jira ticket for follow-up",
    ("medium", "security"): "Review access patterns; update WAF rules if needed",
    ("medium", "performance"): "Collect flame graph; no immediate action required",
    ("low", "infra"): "Log event; no action required",
    ("low", "app"): "No action required",
    ("low", "security"): "Log event; no action required",
    ("low", "performance"): "No action required",
}


def _match(text: str, rules: list[dict], key: str, default: str) -> str:
    text_lower = text.lower()
    for rule in rules:
        if any(kw in text_lower for kw in rule["keywords"]):
            return rule[key]
    return default


def classify_alert(alert: dict) -> dict:
    combined = f"{alert.get('title', '')} {alert.get('description', '')} {alert.get('source', '')}"

    severity = _match(combined, SEVERITY_RULES, "severity", "medium")
    category = _match(combined, CATEGORY_RULES, "category", "app")
    suggested_action = ACTION_MAP.get((severity, category), "Review alert manually")

    return {
        "severity": severity,
        "category": category,
        "suggested_action": suggested_action,
    }

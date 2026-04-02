"""Tests for the alert router."""
from agent.router import route_alert


def test_critical_infra_routes_all():
    classification = {
        "severity": "critical",
        "category": "infra",
        "suggested_action": "Page on-call SRE immediately",
    }
    destinations = route_alert(classification)
    assert "pagerduty" in destinations
    assert "slack" in destinations
    assert "email" in destinations


def test_high_app_routes_slack_only():
    classification = {
        "severity": "high",
        "category": "app",
        "suggested_action": "Review recent deploys",
    }
    destinations = route_alert(classification)
    assert destinations == ["slack"]


def test_low_infra_is_silent():
    classification = {
        "severity": "low",
        "category": "infra",
        "suggested_action": "Log event",
    }
    destinations = route_alert(classification)
    assert destinations == []


def test_medium_security_routes_slack_and_email():
    classification = {
        "severity": "medium",
        "category": "security",
        "suggested_action": "Review access patterns",
    }
    destinations = route_alert(classification)
    assert "slack" in destinations
    assert "email" in destinations

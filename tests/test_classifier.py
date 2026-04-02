"""Tests for the alert classifier."""
import pytest
from agent.classifier import classify_alert


def test_critical_infra():
    alert = {"title": "Node is down", "description": "Host prod-node-01 unreachable", "source": "prod-node-01"}
    result = classify_alert(alert)
    assert result["severity"] == "critical"
    assert result["category"] == "infra"
    assert "suggested_action" in result


def test_critical_app():
    alert = {"title": "Payment service 5xx error rate 100%", "description": "All requests failing", "source": "payment-service"}
    result = classify_alert(alert)
    assert result["severity"] == "critical"
    assert result["category"] == "app"


def test_high_security():
    alert = {"title": "Brute-force login attempts", "description": "403 failed auth in 60s", "source": "auth-service"}
    result = classify_alert(alert)
    assert result["severity"] == "high"
    assert result["category"] == "security"


def test_medium_performance():
    alert = {"title": "API latency degraded", "description": "p99 response time slow on /api", "source": "api-gateway"}
    result = classify_alert(alert)
    assert result["severity"] == "medium"
    assert result["category"] == "performance"


def test_low_deploy():
    alert = {"title": "Deployment started", "description": "CI/CD deploy triggered restart", "source": "recommendation-service"}
    result = classify_alert(alert)
    assert result["severity"] == "low"


def test_unknown_defaults_to_medium_app():
    alert = {"title": "Something odd happened", "description": "", "source": "unknown"}
    result = classify_alert(alert)
    assert result["severity"] == "medium"
    assert result["category"] == "app"

"""Tests for remediator and individual runbooks."""
from agent.remediator import attempt_remediation
from runbooks.rb_infra_01 import RB_INFRA_01
from runbooks.rb_app_01 import RB_APP_01
from runbooks.rb_security_01 import RB_SECURITY_01
from runbooks.rb_perf_01 import RB_PERF_01


def test_infra_runbook_matches_and_executes():
    rb = RB_INFRA_01()
    alert = {"id": "T1", "title": "Node down", "source": "prod-node-01", "metadata": {}}
    assert rb.matches("critical", "infra", alert)
    result = rb.execute(alert)
    assert result["status"] == "executed"
    assert "prod-node-01" in result["action"]


def test_app_runbook_matches_only_critical():
    rb = RB_APP_01()
    alert = {"id": "T2", "title": "5xx", "source": "payment-service", "metadata": {}}
    assert rb.matches("critical", "app", alert)
    assert not rb.matches("high", "app", alert)


def test_security_runbook_blocks_ip():
    rb = RB_SECURITY_01()
    alert = {"id": "T3", "title": "Brute force", "source": "auth-service", "metadata": {"source_ip": "1.2.3.4"}}
    assert rb.matches("critical", "security", alert)
    result = rb.execute(alert)
    assert "1.2.3.4" in result["action"]


def test_perf_runbook_scales_service():
    rb = RB_PERF_01()
    alert = {"id": "T4", "title": "High latency", "source": "api-gateway", "metadata": {}}
    assert rb.matches("high", "performance", alert)
    result = rb.execute(alert)
    assert "api-gateway" in result["action"]


def test_no_runbook_returns_skipped():
    alert = {"id": "T5", "title": "Deploy started", "source": "svc", "metadata": {}}
    classification = {"severity": "low", "category": "app", "suggested_action": ""}
    result = attempt_remediation(alert, classification)
    assert result["status"] == "skipped"
    assert result["runbook_id"] is None


def test_full_pipeline_critical_infra():
    alert = {"id": "T6", "title": "Node OOM killed", "source": "worker-node-01",
             "description": "OOM killer triggered on worker-node-01", "metadata": {}}
    classification = {"severity": "critical", "category": "infra", "suggested_action": "Page SRE"}
    result = attempt_remediation(alert, classification)
    assert result["status"] == "executed"
    assert result["runbook_id"] == "RB-INFRA-01"

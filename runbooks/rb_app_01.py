"""RB-APP-01: Critical app alerts — mock deployment rollback."""
import logging
from runbooks.base import Runbook

logger = logging.getLogger(__name__)


class RB_APP_01(Runbook):
    id = "RB-APP-01"

    def matches(self, severity, category, alert):
        return category == "app" and severity == "critical"

    def execute(self, alert):
        service = alert.get("source", "unknown-service")
        logger.info(f"  [RUNBOOK {self.id}] Simulating deployment rollback for {service}")
        # Mock: would run `kubectl rollout undo deployment/<service>`
        return {
            "status": "executed",
            "action": f"Mock: rolled back deployment for {service} to previous revision",
        }

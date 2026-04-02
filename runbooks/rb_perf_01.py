"""RB-PERF-01: High performance alerts — mock horizontal scale-out."""
import logging
from runbooks.base import Runbook

logger = logging.getLogger(__name__)


class RB_PERF_01(Runbook):
    id = "RB-PERF-01"

    def matches(self, severity, category, alert):
        return category == "performance" and severity in ("critical", "high")

    def execute(self, alert):
        service = alert.get("source", "unknown-service")
        logger.info(f"  [RUNBOOK {self.id}] Simulating horizontal scale-out for {service}")
        # Mock: would run `kubectl scale deployment/<service> --replicas=+2`
        return {
            "status": "executed",
            "action": f"Mock: scaled {service} by +2 replicas via HPA override",
        }

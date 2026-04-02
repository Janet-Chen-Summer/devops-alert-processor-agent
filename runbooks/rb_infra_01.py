"""RB-INFRA-01: High/critical infra alerts — mock node restart."""
import logging
from runbooks.base import Runbook

logger = logging.getLogger(__name__)


class RB_INFRA_01(Runbook):
    id = "RB-INFRA-01"

    def matches(self, severity, category, alert):
        return category == "infra" and severity in ("critical", "high")

    def execute(self, alert):
        node = alert.get("source", "unknown-node")
        logger.info(f"  [RUNBOOK {self.id}] Simulating node health-check restart on {node}")
        # Mock: would run `kubectl drain <node> && kubectl uncordon <node>`
        return {
            "status": "executed",
            "action": f"Mock: drained and uncordoned node {node}",
        }

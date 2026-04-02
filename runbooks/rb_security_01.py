"""RB-SECURITY-01: Security alerts — mock IP block."""
import logging
from runbooks.base import Runbook

logger = logging.getLogger(__name__)


class RB_SECURITY_01(Runbook):
    id = "RB-SECURITY-01"

    def matches(self, severity, category, alert):
        return category == "security" and severity in ("critical", "high")

    def execute(self, alert):
        source_ip = alert.get("metadata", {}).get("source_ip", "0.0.0.0")
        logger.info(f"  [RUNBOOK {self.id}] Simulating WAF block for IP {source_ip}")
        # Mock: would call firewall API to block IP
        return {
            "status": "executed",
            "action": f"Mock: added {source_ip} to WAF blocklist and rotated session tokens",
        }

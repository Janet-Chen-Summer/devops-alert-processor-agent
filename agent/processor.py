"""
DevOps Alert Processor Agent
Classifies → Routes → Remediates alerts using mock data.
"""
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from agent.classifier import classify_alert
from agent.router import route_alert
from agent.remediator import attempt_remediation

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class AlertResult:
    alert_id: str
    title: str
    severity: str
    category: str
    suggested_action: str
    routed_to: list[str]
    remediation: dict
    processed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


def process_alert(alert: dict) -> AlertResult:
    """Full pipeline: classify → route → remediate."""
    alert_id = alert.get("id", "unknown")
    logger.info(f"Processing alert [{alert_id}]: {alert.get('title')}")

    # Step 1: Classify severity and category
    classification = classify_alert(alert)
    logger.info(f"  → Classified: severity={classification['severity']}, category={classification['category']}")

    # Step 2: Route to appropriate mock channels
    destinations = route_alert(classification)
    logger.info(f"  → Routed to: {destinations}")

    # Step 3: Attempt auto-remediation via runbook
    remediation = attempt_remediation(alert, classification)
    logger.info(f"  → Remediation: {remediation['status']} — {remediation['action']}")

    return AlertResult(
        alert_id=alert_id,
        title=alert.get("title", ""),
        severity=classification["severity"],
        category=classification["category"],
        suggested_action=classification["suggested_action"],
        routed_to=destinations,
        remediation=remediation,
    )


def process_all(alerts: list[dict]) -> list[AlertResult]:
    results = []
    for alert in alerts:
        try:
            result = process_alert(alert)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process alert {alert.get('id')}: {e}")
    return results


def results_to_dict(results: list[AlertResult]) -> list[dict]:
    return [r.__dict__ for r in results]

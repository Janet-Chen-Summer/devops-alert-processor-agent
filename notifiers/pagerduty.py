"""Mock PagerDuty notifier — prints incident payload instead of calling the API."""
import logging

logger = logging.getLogger(__name__)

URGENCY_MAP = {"critical": "high", "high": "high", "medium": "low", "low": "low"}


def send_pagerduty(classification: dict) -> None:
    payload = {
        "routing_key": "MOCK_PAGERDUTY_KEY",
        "event_action": "trigger",
        "payload": {
            "summary": f"[{classification['severity'].upper()}] {classification['category']} alert",
            "severity": classification["severity"],
            "source": "devops-alert-agent",
            "custom_details": {"action": classification["suggested_action"]},
        },
    }
    urgency = URGENCY_MAP.get(classification["severity"], "low")
    logger.info(f"  [MOCK PagerDuty | urgency={urgency}] {payload['payload']['summary']}")

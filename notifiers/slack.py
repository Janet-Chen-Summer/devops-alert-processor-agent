"""Mock Slack notifier — prints a formatted payload instead of calling the API."""
import logging

logger = logging.getLogger(__name__)

CHANNEL_MAP = {
    "critical": "#incidents",
    "high":     "#alerts-high",
    "medium":   "#alerts-medium",
    "low":      "#alerts-low",
}


def send_slack(classification: dict) -> None:
    channel = CHANNEL_MAP.get(classification["severity"], "#alerts")
    payload = {
        "channel": channel,
        "text": (
            f"[{classification['severity'].upper()}] {classification['category'].upper()} alert\n"
            f"Action: {classification['suggested_action']}"
        ),
    }
    logger.info(f"  [MOCK Slack → {channel}] {payload['text'][:80]}")

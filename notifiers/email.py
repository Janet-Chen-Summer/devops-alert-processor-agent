"""Mock email notifier — prints email payload instead of sending via SMTP."""
import logging

logger = logging.getLogger(__name__)

RECIPIENTS = {
    "security":    ["security-team@example.com", "oncall@example.com"],
    "infra":       ["infra-team@example.com"],
    "app":         ["dev-team@example.com"],
    "performance": ["dev-team@example.com"],
}


def send_email(classification: dict) -> None:
    to = RECIPIENTS.get(classification["category"], ["oncall@example.com"])
    subject = f"[{classification['severity'].upper()}] DevOps Alert — {classification['category']}"
    body = (
        f"Severity : {classification['severity']}\n"
        f"Category : {classification['category']}\n"
        f"Action   : {classification['suggested_action']}"
    )
    logger.info(f"  [MOCK Email → {', '.join(to)}] {subject}")
    logger.debug(f"  Body:\n{body}")

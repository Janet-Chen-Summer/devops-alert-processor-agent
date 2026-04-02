"""
Runbook registry — discovers and matches runbooks to alerts.
"""
from runbooks.rb_infra_01 import RB_INFRA_01
from runbooks.rb_app_01 import RB_APP_01
from runbooks.rb_security_01 import RB_SECURITY_01
from runbooks.rb_perf_01 import RB_PERF_01

ALL_RUNBOOKS = [RB_INFRA_01(), RB_APP_01(), RB_SECURITY_01(), RB_PERF_01()]


def find_runbook(severity: str, category: str, alert: dict):
    """Return first matching runbook or None."""
    for rb in ALL_RUNBOOKS:
        if rb.matches(severity, category, alert):
            return rb
    return None

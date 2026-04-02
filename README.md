# DevOps Alert Processor Agent

A lightweight Python POC that simulates an intelligent DevOps alert-processing pipeline. Drop in mock alerts, get severity classification, smart routing to mock channels, and automated runbook remediation — all in one clean flow.

---

## What it does

```
Alert JSON  →  Classify  →  Route  →  Remediate
               (severity,   (Slack,    (runbooks:
                category)    PagerDuty, restart, rollback,
                             Email)     block IP, scale out)
```

**Three stages:**

1. **Classify** — keyword rules assign a `severity` (critical / high / medium / low) and `category` (infra / app / security / performance), plus a human-readable suggested action.
2. **Route** — a routing matrix maps (severity × category) → mock notifiers. Mock Slack, PagerDuty, and email payloads are printed to stdout (no real API keys needed).
3. **Remediate** — four runbooks match on severity + category and simulate real actions: node drain/uncordon, deployment rollback, WAF IP block, and HPA scale-out.

---

## Project layout

```
devops-alert-agent/
├── agent/
│   ├── classifier.py      # Severity + category classification
│   ├── router.py          # Routing matrix + notifier dispatch
│   ├── remediator.py      # Runbook lookup + execution
│   └── processor.py       # Orchestrates the full pipeline
├── notifiers/
│   ├── slack.py           # Mock Slack notifier
│   ├── pagerduty.py       # Mock PagerDuty notifier
│   └── email.py           # Mock email notifier
├── runbooks/
│   ├── base.py            # Abstract Runbook base class
│   ├── registry.py        # Runbook discovery + matching
│   ├── rb_infra_01.py     # Node drain/uncordon
│   ├── rb_app_01.py       # Deployment rollback
│   ├── rb_security_01.py  # WAF IP block
│   └── rb_perf_01.py      # HPA scale-out
├── mock_data/
│   └── alerts.json        # 8 realistic mock alerts
├── tests/
│   ├── test_classifier.py
│   ├── test_router.py
│   └── test_remediator.py
├── main.py                # Entrypoint
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Quickstart

### Prerequisites
- Docker + Docker Compose (v2)

### Run the agent

```bash
git clone <your-repo-url>
cd devops-alert-agent

docker compose up --build
```

You'll see each alert processed with its classification, routing decisions, and remediation outcome. A full JSON summary is written inside the container at `/tmp/alert_results.json`.

### Run the tests

```bash
docker compose --profile test run --rm test
```

### Run locally (no Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Adding your own alerts

Edit `mock_data/alerts.json`. Each alert follows this schema:

```json
{
  "id":          "ALT-XXX",
  "title":       "Short human-readable title",
  "description": "Longer description with technical context",
  "source":      "service-or-host-name",
  "timestamp":   "2025-04-02T00:00:00Z",
  "metadata":    { "source_ip": "optional extra fields" }
}
```

## Adding a new runbook

1. Create `runbooks/rb_your_name.py` extending `Runbook`
2. Implement `matches(severity, category, alert) -> bool`
3. Implement `execute(alert) -> {"status": ..., "action": ...}`
4. Register it in `runbooks/registry.py`

---

## Design decisions

- **No external dependencies** beyond `pytest` — zero API keys, zero cloud accounts needed to run.
- **Keyword-based classifier** — intentionally simple; replace with an ML model or LLM call without touching the router or runbooks.
- **Routing matrix** — explicit and reviewable; changing alert routing is a one-line table edit.
- **Runbook pattern** — each runbook is independently testable and swappable for real `subprocess` / `kubectl` / API calls.

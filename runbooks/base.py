"""Abstract base for all runbooks."""
from abc import ABC, abstractmethod


class Runbook(ABC):
    id: str = "RB-BASE"

    @abstractmethod
    def matches(self, severity: str, category: str, alert: dict) -> bool:
        ...

    @abstractmethod
    def execute(self, alert: dict) -> dict:
        ...

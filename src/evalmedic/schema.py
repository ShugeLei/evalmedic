"""Typed measurement metadata for evaluation runs.

The schema is intentionally small. Framework adapters may attach additional
metadata, but the versions needed for regression diagnosis stay explicit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any, Mapping


class Component(str, Enum):
    """Components that can create an evaluation regression."""

    MODEL = "model"
    PROMPT = "prompt"
    TOOL_RUNTIME = "tool_runtime"
    HARNESS_DATA = "harness_data"
    EVALUATOR = "evaluator"


@dataclass(frozen=True)
class MeasurementManifest:
    """Versions of the system and measuring instrument used for one run."""

    model: str
    prompt: str
    tool_runtime: str
    harness_data: str
    evaluator: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "model",
            "prompt",
            "tool_runtime",
            "harness_data",
            "evaluator",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} version must be a non-empty string")

    def changed_components(
        self, baseline: "MeasurementManifest"
    ) -> frozenset[Component]:
        """Return components whose version differs from a baseline manifest."""

        changed: set[Component] = set()
        if self.model != baseline.model:
            changed.add(Component.MODEL)
        if self.prompt != baseline.prompt:
            changed.add(Component.PROMPT)
        if self.tool_runtime != baseline.tool_runtime:
            changed.add(Component.TOOL_RUNTIME)
        if self.harness_data != baseline.harness_data:
            changed.add(Component.HARNESS_DATA)
        if self.evaluator != baseline.evaluator:
            changed.add(Component.EVALUATOR)
        return frozenset(changed)


@dataclass(frozen=True)
class Outcome:
    """Minimal outcome needed by the initial deterministic benchmark."""

    task_id: str
    score: float
    passed: bool | None = None
    latency_ms: float | None = None
    token_count: int | None = None

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id must be non-empty")
        if not isfinite(self.score):
            raise ValueError("score must be finite")
        if self.latency_ms is not None and self.latency_ms < 0:
            raise ValueError("latency_ms cannot be negative")
        if self.token_count is not None and self.token_count < 0:
            raise ValueError("token_count cannot be negative")


@dataclass(frozen=True)
class EvaluationRecord:
    """One task outcome plus the manifest that produced it."""

    run_id: str
    release_id: str
    manifest: MeasurementManifest
    outcome: Outcome

    def __post_init__(self) -> None:
        if not self.run_id.strip():
            raise ValueError("run_id must be non-empty")
        if not self.release_id.strip():
            raise ValueError("release_id must be non-empty")


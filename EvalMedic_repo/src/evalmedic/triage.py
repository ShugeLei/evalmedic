"""Counterfactual replay evidence for evaluation-regression diagnosis."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import fmean
from typing import Iterable

from .schema import Component


@dataclass(frozen=True)
class ReplayEvidence:
    """Score after replacing one candidate component with its baseline version.

    Scores are assumed to be oriented so that higher is better. Multiple replay
    observations for one component are averaged by ``diagnose_regression``.
    """

    component: Component
    replay_score: float
    replay_faithful: bool = True
    note: str = ""

    def __post_init__(self) -> None:
        if not isfinite(self.replay_score):
            raise ValueError("replay_score must be finite")


@dataclass(frozen=True)
class RankedCause:
    component: Component
    support: float
    evidence_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "component": self.component.value,
            "support": round(self.support, 6),
            "evidence_count": self.evidence_count,
        }


@dataclass(frozen=True)
class Diagnosis:
    baseline_score: float
    candidate_score: float
    ranked_causes: tuple[RankedCause, ...]
    abstained: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "baseline_score": self.baseline_score,
            "candidate_score": self.candidate_score,
            "abstained": self.abstained,
            "reason": self.reason,
            "ranked_causes": [cause.to_dict() for cause in self.ranked_causes],
        }


def diagnose_regression(
    baseline_score: float,
    candidate_score: float,
    evidence: Iterable[ReplayEvidence],
    *,
    min_support: float = 0.5,
    min_margin: float = 0.1,
) -> Diagnosis:
    """Rank component hypotheses from counterfactual recovery evidence.

    Support is the fraction of the observed regression recovered when a single
    component is restored to its baseline version, clipped to ``[0, 1]``.
    The function abstains when there is no regression, no faithful evidence,
    insufficient recovery, or an ambiguous top-two margin.
    """

    for name, value in (
        ("baseline_score", baseline_score),
        ("candidate_score", candidate_score),
        ("min_support", min_support),
        ("min_margin", min_margin),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if not 0 <= min_support <= 1:
        raise ValueError("min_support must be within [0, 1]")
    if not 0 <= min_margin <= 1:
        raise ValueError("min_margin must be within [0, 1]")

    regression = baseline_score - candidate_score
    if regression <= 0:
        return Diagnosis(
            baseline_score=baseline_score,
            candidate_score=candidate_score,
            ranked_causes=(),
            abstained=True,
            reason="candidate score does not show a regression",
        )

    grouped: dict[Component, list[float]] = {}
    for item in evidence:
        if not item.replay_faithful:
            continue
        recovery = (item.replay_score - candidate_score) / regression
        grouped.setdefault(item.component, []).append(max(0.0, min(1.0, recovery)))

    ranked = tuple(
        sorted(
            (
                RankedCause(
                    component=component,
                    support=fmean(values),
                    evidence_count=len(values),
                )
                for component, values in grouped.items()
            ),
            key=lambda cause: (-cause.support, cause.component.value),
        )
    )

    if not ranked:
        return Diagnosis(
            baseline_score=baseline_score,
            candidate_score=candidate_score,
            ranked_causes=(),
            abstained=True,
            reason="no faithful counterfactual replay evidence",
        )

    top = ranked[0]
    if top.support < min_support:
        return Diagnosis(
            baseline_score=baseline_score,
            candidate_score=candidate_score,
            ranked_causes=ranked,
            abstained=True,
            reason="no component recovered enough of the observed regression",
        )

    if len(ranked) > 1 and top.support - ranked[1].support < min_margin:
        return Diagnosis(
            baseline_score=baseline_score,
            candidate_score=candidate_score,
            ranked_causes=ranked,
            abstained=True,
            reason="top component hypotheses are not sufficiently separated",
        )

    return Diagnosis(
        baseline_score=baseline_score,
        candidate_score=candidate_score,
        ranked_causes=ranked,
        abstained=False,
        reason=f"{top.component.value} has the strongest counterfactual recovery evidence",
    )


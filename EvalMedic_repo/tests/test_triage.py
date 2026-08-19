import pytest

from evalmedic.schema import Component
from evalmedic.triage import ReplayEvidence, diagnose_regression


def test_diagnoses_component_with_strong_recovery() -> None:
    diagnosis = diagnose_regression(
        baseline_score=0.9,
        candidate_score=0.4,
        evidence=[
            ReplayEvidence(Component.MODEL, replay_score=0.86),
            ReplayEvidence(Component.PROMPT, replay_score=0.44),
            ReplayEvidence(Component.TOOL_RUNTIME, replay_score=0.41),
        ],
    )

    assert not diagnosis.abstained
    assert diagnosis.ranked_causes[0].component is Component.MODEL
    assert diagnosis.ranked_causes[0].support == pytest.approx(0.92)


def test_abstains_when_top_hypotheses_are_ambiguous() -> None:
    diagnosis = diagnose_regression(
        baseline_score=1.0,
        candidate_score=0.5,
        evidence=[
            ReplayEvidence(Component.MODEL, replay_score=0.9),
            ReplayEvidence(Component.PROMPT, replay_score=0.88),
        ],
        min_margin=0.1,
    )

    assert diagnosis.abstained
    assert "not sufficiently separated" in diagnosis.reason


def test_ignores_unfaithful_replays() -> None:
    diagnosis = diagnose_regression(
        baseline_score=1.0,
        candidate_score=0.5,
        evidence=[
            ReplayEvidence(
                Component.TOOL_RUNTIME,
                replay_score=1.0,
                replay_faithful=False,
            )
        ],
    )

    assert diagnosis.abstained
    assert diagnosis.ranked_causes == ()
    assert "no faithful" in diagnosis.reason


def test_abstains_when_candidate_did_not_regress() -> None:
    diagnosis = diagnose_regression(
        baseline_score=0.8,
        candidate_score=0.9,
        evidence=[ReplayEvidence(Component.MODEL, replay_score=0.8)],
    )

    assert diagnosis.abstained
    assert "does not show a regression" in diagnosis.reason


def test_averages_repeated_evidence() -> None:
    diagnosis = diagnose_regression(
        baseline_score=1.0,
        candidate_score=0.5,
        evidence=[
            ReplayEvidence(Component.MODEL, replay_score=1.0),
            ReplayEvidence(Component.MODEL, replay_score=0.75),
            ReplayEvidence(Component.PROMPT, replay_score=0.55),
        ],
    )

    assert diagnosis.ranked_causes[0].component is Component.MODEL
    assert diagnosis.ranked_causes[0].support == pytest.approx(0.75)
    assert diagnosis.ranked_causes[0].evidence_count == 2


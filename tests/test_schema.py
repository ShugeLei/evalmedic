import pytest

from evalmedic.schema import Component, MeasurementManifest, Outcome


def manifest(**overrides: str) -> MeasurementManifest:
    values = {
        "model": "model-v1",
        "prompt": "prompt-v1",
        "tool_runtime": "tools-v1",
        "harness_data": "suite-v1",
        "evaluator": "judge-v1",
    }
    values.update(overrides)
    return MeasurementManifest(**values)


def test_changed_components_are_explicit() -> None:
    baseline = manifest()
    candidate = manifest(model="model-v2", evaluator="judge-v2")

    assert candidate.changed_components(baseline) == frozenset(
        {Component.MODEL, Component.EVALUATOR}
    )


def test_manifest_rejects_missing_versions() -> None:
    with pytest.raises(ValueError, match="prompt version"):
        manifest(prompt="")


def test_outcome_rejects_nonfinite_score() -> None:
    with pytest.raises(ValueError, match="score must be finite"):
        Outcome(task_id="task-1", score=float("nan"))


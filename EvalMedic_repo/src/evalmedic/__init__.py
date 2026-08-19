"""Public interfaces for the EvalMedic research prototype."""

from .schema import Component, EvaluationRecord, MeasurementManifest, Outcome
from .triage import Diagnosis, RankedCause, ReplayEvidence, diagnose_regression

__all__ = [
    "Component",
    "Diagnosis",
    "EvaluationRecord",
    "MeasurementManifest",
    "Outcome",
    "RankedCause",
    "ReplayEvidence",
    "diagnose_regression",
]

__version__ = "0.1.0"


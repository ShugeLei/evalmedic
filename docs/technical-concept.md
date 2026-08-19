# Technical concept

## Core thesis

An evaluation system is a measurement instrument. It must be selected, versioned, calibrated, diagnosed, and maintained rather than merely executed.

## Non-goals

- Building another general-purpose evaluation runner.
- Replacing execution, tracing, or observability platforms.
- Claiming that LLM judges can be made fully reliable.
- Acting as an autonomous ship/no-ship authority in the initial version.
- Claiming academic novelty before related-work review and empirical validation.

## Canonical measurement manifest

Every evaluation record should identify:

- release and run identity;
- model/checkpoint and decoding configuration;
- prompt, scaffold, and context-policy versions;
- tool schema, runtime, retrieval, and dependency versions;
- harness and dataset versions;
- grader model, rubric, prompt, and reference-set versions;
- task slice and trace identity;
- deterministic, grader, confidence, abstention, and human outcomes; and
- latency, token, retry, cost, and wall-clock measurements.

The public scaffold implements a small typed core. Adapters can add framework-specific metadata without changing the diagnosis interface.

## Counterfactual regression triage

The V0.1 mechanism freezes most of the system and swaps one component back to its baseline version. Recovery after a component swap supports that component as a cause of the observed regression.

This is an evidence procedure, not guaranteed causal identification. Components may interact, replay may be unfaithful, and external state may be unavailable. EvalMedic therefore produces ranked support plus explicit abstention rather than a falsely precise probability.

## Evaluator drift calibration

A frozen bridge set of trajectories should be rescored by old and new evaluator versions. Comparability checks include overall and slice-level agreement, bias shift, variance, rank reversals, false positives/negatives against deterministic or human anchors, and confidence calibration where available.

A mapping between evaluator versions should be fitted only when empirical evidence supports transport. Otherwise the release should establish a new score baseline.

## Adaptive evaluation planning

Future work will use historical test sensitivity, redundancy, recent failure history, severity, and expected information gain to select a first-stage subset. A sequential policy requests more tests when confidence is insufficient. Hard mandatory tests are never removed by statistical optimization.

## Benchmark maintenance

Candidate failures are scored by frequency, severity, coverage gap, discriminative power, redundancy, saturation, and stability. The system recommends PROMOTE, MERGE, RETAIN AS DIAGNOSTIC, or RETIRE; human approval remains required in the initial design.


# EvalMedic roadmap

The roadmap separates implementation milestones from research claims. A milestone is complete only when its tests and evidence artifacts are present.

## V0.1 - controlled regression diagnosis

- [x] Canonical measurement manifest
- [x] Component-version differencing
- [x] Minimal counterfactual evidence model
- [x] Ranked hypotheses with abstention
- [x] JSON CLI example
- [ ] Inspect AI log adapter
- [ ] Thirty-task deterministic micro-benchmark
- [ ] Controlled R0-R4 release generator
- [ ] Grader bridge/anchor set
- [ ] End-to-end top-1/top-k diagnosis evaluation
- [ ] HTML and JSON evidence reports

Claim to earn: for controlled perturbations with known causes, EvalMedic can identify the responsible component or abstain when the evidence is ambiguous.

## V0.2 - adaptive evaluation planning

- [ ] Historical release-by-test sensitivity matrix
- [ ] Redundancy and representation-similarity baselines
- [ ] Risk-aware sequential subset policy
- [ ] Mandatory-test constraints
- [ ] Stopping-rule calibration

Claim to earn: meaningful regression recall can be preserved while materially reducing suite size, cost, or time-to-decision.

## V0.3 - benchmark maintenance

- [ ] Production-failure clustering
- [ ] Novelty, severity, stability, and redundancy signals
- [ ] PROMOTE / MERGE / RETAIN AS DIAGNOSTIC / RETIRE recommendations
- [ ] Human approval workflow
- [ ] Longitudinal compactness and future-failure detection study

Claim to earn: production failures improve benchmark coverage without uncontrolled suite growth.

## V1.0 - external integration

- [ ] LangSmith adapter
- [ ] Braintrust adapter
- [ ] Custom JSON adapter
- [ ] CI integration
- [ ] Evidence review UI
- [ ] External user study with evaluation engineers

Claim to earn: the diagnosis-and-decision layer is useful outside the controlled prototype.

## Falsification criteria

Narrow or stop the project if:

- component interactions make controlled replay routinely non-identifiable;
- replay fidelity is too poor to distinguish changes;
- abstention dominates useful diagnoses;
- simple agreement checks match grader-drift methods;
- adaptive planning needs nearly the full suite to preserve recall; or
- the system does not reduce engineering effort beyond competent manual trace analysis.


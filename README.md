# EvalMedic

**Diagnosis, calibration, and maintenance for LLM and agent evaluation systems.**

EvalMedic is an evaluation infrastructure project for the work that begins after a metric changes. It is designed as a diagnosis-and-decision layer above existing evaluation runners and observability systems.

> Do not only evaluate the model. Continuously evaluate and maintain the measurement system.

## Why this project

Current tools are good at running evaluations, logging trajectories, scoring outputs, and showing regressions. An evaluation engineer still has to determine:

- whether the regression is real or measurement noise;
- whether the model, prompt, tool/runtime, harness/data, or evaluator changed the result;
- whether old and new judge scores remain comparable;
- which additional tests would most reduce uncertainty; and
- whether a new production failure should become a durable evaluation.

EvalMedic turns those questions into versioned metadata, controlled replay experiments, explicit evidence, and uncertainty-aware abstention.

## Status

EvalMedic is an early research-engineering prototype.

Implemented in this public scaffold:

- typed, versioned measurement manifests;
- component-level change detection;
- a minimal counterfactual replay evidence model;
- ranked root-cause hypotheses with explicit abstention;
- a JSON command-line example; and
- unit tests for the core diagnosis behavior.

Not yet implemented:

- Inspect AI or other trace adapters;
- agent trajectory execution;
- grader bridge-set calibration;
- adaptive eval planning;
- benchmark promotion/merge/retire workflows; and
- empirical validation on the planned controlled-release benchmark.

Planned scope and achieved results are kept separate throughout the repository.

## Positioning

EvalMedic is **not** a replacement for Inspect AI, LangSmith, Braintrust, OpenAI Evals, or an internal evaluation platform. Those systems remain responsible for execution, tracing, and scoring. EvalMedic consumes their artifacts and produces diagnosis and decision evidence.

```text
existing eval stack
  -> versioned measurement manifest
  -> controlled counterfactual replay
  -> ranked root-cause evidence
  -> abstain or recommend the next investigation
```

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
pytest
```

Run the included controlled-replay example:

```bash
evalmedic diagnose examples/model_regression.json
```

Example output:

```json
{
  "abstained": false,
  "reason": "model has the strongest counterfactual recovery evidence",
  "ranked_causes": [
    {"component": "model", "support": 0.92},
    {"component": "prompt", "support": 0.08}
  ]
}
```

## V0.1 validation plan

The first empirical release will use deterministic tasks with known perturbations:

| Slice | Tasks | Ground truth |
| --- | ---: | --- |
| Tool calling | 10 | Expected function and arguments |
| SQL | 10 | Deterministic query/result checks |
| File or coding tasks | 10 | File assertions and unit tests |

Controlled release conditions:

| Condition | Change | Known cause |
| --- | --- | --- |
| R0 | Baseline | None |
| R1 | Model/checkpoint only | Model |
| R2 | Prompt/scaffold only | Prompt |
| R3 | Tool schema/runtime only | Tool/runtime |
| R4 | Judge/rubric only, using frozen traces | Evaluator |

The planned initial envelope is 30 tasks x 5 conditions x 2 repeats, or approximately 300 trajectories. These are **design targets, not reported results**.

Primary metrics will include top-1 root-cause accuracy, top-k cause recall, regression recall, diagnosis latency, replay count, abstention rate, and calibration.

## Repository map

```text
src/evalmedic/
  schema.py       canonical measurement manifest
  triage.py       counterfactual evidence and diagnosis
  cli.py          minimal JSON command line
tests/            unit tests for schema and triage behavior
examples/         controlled replay input examples
docs/             technical concept and design boundaries
ROADMAP.md        staged implementation and falsification criteria
```

## Design principles

1. **Version the measuring instrument.** A score is uninterpretable without the model, prompt, tools, runtime, data, harness, and evaluator versions that produced it.
2. **Prefer controlled evidence to confident stories.** Replay one component at a time when possible and expose interactions when not.
3. **Abstain when the cause is not identifiable.** A ranked list is not a causal guarantee.
4. **Keep mandatory safety tests.** Cost optimization must never prune critical tests merely because they appear redundant.
5. **Earn claims empirically.** The project should be narrowed or stopped if it does not reduce real evaluation-engineering effort.

## Project page

The project narrative and validation plan are available at [shugelei.github.io/projects/evalmedic.html](https://shugelei.github.io/projects/evalmedic.html).

## Author

Shuge Lei — [website](https://shugelei.github.io) · [GitHub](https://github.com/ShugeLei)


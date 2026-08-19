"""Minimal command line for controlled replay evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .schema import Component
from .triage import ReplayEvidence, diagnose_regression


def _load_diagnosis(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    evidence = [
        ReplayEvidence(
            component=Component(item["component"]),
            replay_score=float(item["replay_score"]),
            replay_faithful=bool(item.get("replay_faithful", True)),
            note=str(item.get("note", "")),
        )
        for item in payload["replays"]
    ]
    diagnosis = diagnose_regression(
        baseline_score=float(payload["baseline_score"]),
        candidate_score=float(payload["candidate_score"]),
        evidence=evidence,
        min_support=float(payload.get("min_support", 0.5)),
        min_margin=float(payload.get("min_margin", 0.1)),
    )
    return diagnosis.to_dict()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evalmedic")
    subparsers = parser.add_subparsers(dest="command", required=True)
    diagnose = subparsers.add_parser(
        "diagnose", help="rank root-cause hypotheses from controlled replay scores"
    )
    diagnose.add_argument("input", type=Path, help="JSON replay evidence file")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "diagnose":
        print(json.dumps(_load_diagnosis(args.input), indent=2, sort_keys=True))
        return 0
    raise AssertionError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())


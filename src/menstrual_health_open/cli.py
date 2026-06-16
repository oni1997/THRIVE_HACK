from __future__ import annotations

import argparse
import json
import sys

from menstrual_health_open.synthetic import iter_records, write_csv, write_jsonl
from menstrual_health_open.validation import validate_file, load_records
from menstrual_health_open.risk_model import score_all_conditions, risk_level
from menstrual_health_open.triage import triage_record, triage_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Menstrual Health Open utilities.")
    subparsers = parser.add_subparsers(dest="command")

    generate = subparsers.add_parser("generate", help="Generate synthetic records.")
    generate.add_argument("--count", type=int, default=100)
    generate.add_argument("--seed", type=int, default=42)
    generate.add_argument("--missingness", type=float, default=0.0)
    generate.add_argument("--conditions", action="store_true",
                          help="Include ground-truth condition labels and free-text symptoms")
    generate.add_argument("--output", default="synthetic-data/generated.csv")
    generate.add_argument("--format", choices=["csv", "jsonl"], default="csv")

    validate = subparsers.add_parser("validate", help="Validate a CSV or JSONL dataset.")
    validate.add_argument("path")

    risk = subparsers.add_parser("risk-score", help="Score risk for a single record (JSON).")
    risk.add_argument("record_json", help="Record as a JSON string")

    triage = subparsers.add_parser("triage", help="Run CHW triage on a CSV/JSONL dataset.")
    triage.add_argument("path")
    triage.add_argument("--max", type=int, default=10, help="Max records to triage")

    return parser


def generate_command(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic menstrual health records.")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--missingness", type=float, default=0.0)
    parser.add_argument("--conditions", action="store_true",
                        help="Include ground-truth condition labels and free-text symptoms")
    parser.add_argument("--output", default="synthetic-data/generated.csv")
    parser.add_argument("--format", choices=["csv", "jsonl"], default="csv")
    args = parser.parse_args(argv)
    return _generate(args)


def validate_command(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a CSV or JSONL dataset.")
    parser.add_argument("path")
    args = parser.parse_args(argv)
    return _validate(args)


def risk_command(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score risk for a single record (JSON).")
    parser.add_argument("record_json")
    args = parser.parse_args(argv)
    return _risk(args)


def triage_command(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run CHW triage on a CSV/JSONL dataset.")
    parser.add_argument("path")
    parser.add_argument("--max", type=int, default=10)
    args = parser.parse_args(argv)
    return _triage(args)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "generate":
        return _generate(args)
    if args.command == "validate":
        return _validate(args)
    if args.command == "risk-score":
        return _risk(args)
    if args.command == "triage":
        return _triage(args)
    parser.print_help()
    return 2


def _generate(args: argparse.Namespace) -> int:
    records = iter_records(args.count, seed=args.seed, missingness=args.missingness,
                           include_conditions=args.conditions)
    output = write_jsonl(records, args.output) if args.format == "jsonl" else write_csv(records, args.output)
    print(json.dumps({"output": str(output), "count": args.count, "format": args.format}, sort_keys=True))
    return 0


def _validate(args: argparse.Namespace) -> int:
    report = validate_file(args.path)
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.valid else 1


def _risk(args: argparse.Namespace) -> int:
    record = json.loads(args.record_json)
    scores = score_all_conditions(record)
    output = {name: {"score": s, "risk": risk_level(s)} for name, s in scores.items()}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


def _triage(args: argparse.Namespace) -> int:
    records = load_records(args.path)
    count = 0
    for record in records:
        if count >= args.max:
            break
        print(triage_summary(record))
        print("---")
        count += 1
    print(json.dumps({"triaged": count, "source": str(args.path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

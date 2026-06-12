from __future__ import annotations

import argparse
import json
import sys

from menstrual_health_open.synthetic import iter_records, write_csv, write_jsonl
from menstrual_health_open.validation import validate_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Menstrual Health Open utilities.")
    subparsers = parser.add_subparsers(dest="command")

    generate = subparsers.add_parser("generate", help="Generate synthetic records.")
    generate.add_argument("--count", type=int, default=100)
    generate.add_argument("--seed", type=int, default=42)
    generate.add_argument("--missingness", type=float, default=0.0)
    generate.add_argument("--output", default="synthetic-data/generated.csv")
    generate.add_argument("--format", choices=["csv", "jsonl"], default="csv")

    validate = subparsers.add_parser("validate", help="Validate a CSV or JSONL dataset.")
    validate.add_argument("path")

    return parser


def generate_command(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic menstrual health records.")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--missingness", type=float, default=0.0)
    parser.add_argument("--output", default="synthetic-data/generated.csv")
    parser.add_argument("--format", choices=["csv", "jsonl"], default="csv")
    args = parser.parse_args(argv)
    return _generate(args)


def validate_command(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a CSV or JSONL dataset.")
    parser.add_argument("path")
    args = parser.parse_args(argv)
    return _validate(args)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "generate":
        return _generate(args)
    if args.command == "validate":
        return _validate(args)
    parser.print_help()
    return 2


def _generate(args: argparse.Namespace) -> int:
    records = iter_records(args.count, seed=args.seed, missingness=args.missingness)
    output = write_jsonl(records, args.output) if args.format == "jsonl" else write_csv(records, args.output)
    print(json.dumps({"output": str(output), "count": args.count, "format": args.format}, sort_keys=True))
    return 0


def _validate(args: argparse.Namespace) -> int:
    report = validate_file(args.path)
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.valid else 1


if __name__ == "__main__":
    sys.exit(main())

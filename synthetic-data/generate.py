#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from menstrual_health_open.synthetic import iter_records, write_csv, write_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic menstrual health records.")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--missingness", type=float, default=0.0)
    parser.add_argument("--format", choices=["csv", "jsonl"], default="csv")
    parser.add_argument("--output", default="synthetic-data/generated.csv")
    args = parser.parse_args()

    records = iter_records(args.count, seed=args.seed, missingness=args.missingness)
    output = write_jsonl(records, args.output) if args.format == "jsonl" else write_csv(records, args.output)
    print(json.dumps({"output": str(output), "count": args.count, "format": args.format}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

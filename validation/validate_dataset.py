#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from menstrual_health_open.validation import validate_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a CSV or JSONL menstrual health dataset.")
    parser.add_argument("path")
    args = parser.parse_args()

    report = validate_file(args.path)
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

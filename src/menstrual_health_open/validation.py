from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "schema_version",
    "record_id",
    "age_band",
    "country_code",
    "setting",
    "collection_month",
    "cycle_length_days",
    "period_duration_days",
    "flow_heaviness",
    "pain_score",
    "missed_school_or_work",
    "product_access",
    "healthcare_access",
    "collection_method",
    "source_type",
]

ENUMS = {
    "age_band": {"10-14", "15-19", "20-24", "25-34", "35-44", "45-54"},
    "setting": {"urban", "peri_urban", "rural"},
    "flow_heaviness": {"light", "moderate", "heavy", "very_heavy"},
    "missed_school_or_work": {"yes", "no", "unknown"},
    "product_access": {"reliable", "sometimes_limited", "often_limited", "unknown"},
    "healthcare_access": {"visited_provider", "wanted_but_could_not_access", "not_needed", "unknown"},
    "collection_method": {"mobile_form", "paper_form", "chw_interview", "web_form"},
    "source_type": {"synthetic", "example", "aggregate"},
}

NUMERIC_RANGES = {
    "cycle_length_days": (15, 60),
    "period_duration_days": (1, 14),
    "pain_score": (0, 10),
}

SUPPORTED_SCHEMA_VERSIONS = {"0.1.0"}


@dataclass(slots=True)
class ValidationError:
    row: int
    field: str
    message: str


@dataclass(slots=True)
class ValidationReport:
    path: str
    row_count: int
    valid: bool
    completeness_score: float
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "row_count": self.row_count,
            "valid": self.valid,
            "completeness_score": self.completeness_score,
            "error_count": len(self.errors),
            "errors": [error.__dict__ for error in self.errors],
            "warnings": self.warnings,
        }


def load_records(path: str | Path) -> list[dict[str, str]]:
    input_path = Path(path)
    if input_path.suffix.lower() == ".jsonl":
        return _load_jsonl(input_path)
    return _load_csv(input_path)


def validate_file(path: str | Path) -> ValidationReport:
    input_path = Path(path)
    records = load_records(input_path)
    errors: list[ValidationError] = []
    filled_required = 0
    possible_required = max(len(records) * len(REQUIRED_FIELDS), 1)

    seen_ids: set[str] = set()
    for index, record in enumerate(records, start=2):
        for field_name in REQUIRED_FIELDS:
            value = str(record.get(field_name, "")).strip()
            if value:
                filled_required += 1
            else:
                errors.append(ValidationError(index, field_name, "required field is missing"))

        record_id = str(record.get("record_id", "")).strip()
        if record_id:
            if record_id in seen_ids:
                errors.append(ValidationError(index, "record_id", "duplicate record_id"))
            seen_ids.add(record_id)

        _validate_country(index, record, errors)
        _validate_schema_version(index, record, errors)
        _validate_month(index, record, errors)
        _validate_enums(index, record, errors)
        _validate_numbers(index, record, errors)

    warnings = []
    if records and any(str(row.get("source_type", "")).strip() != "synthetic" for row in records):
        warnings.append("dataset includes non-synthetic source_type values; confirm this is intentional")

    completeness = round(filled_required / possible_required, 3)
    return ValidationReport(
        path=str(input_path),
        row_count=len(records),
        valid=not errors,
        completeness_score=completeness,
        errors=errors,
        warnings=warnings,
    )


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _load_jsonl(path: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                payload = json.loads(line)
                records.append({key: str(value) for key, value in payload.items()})
    return records


def _validate_country(row: int, record: dict[str, str], errors: list[ValidationError]) -> None:
    value = str(record.get("country_code", "")).strip()
    if value and not re.fullmatch(r"[A-Z]{2}", value):
        errors.append(ValidationError(row, "country_code", "expected ISO 3166-1 alpha-2 code"))


def _validate_schema_version(row: int, record: dict[str, str], errors: list[ValidationError]) -> None:
    value = str(record.get("schema_version", "")).strip()
    if value and value not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append(
            ValidationError(
                row,
                "schema_version",
                f"expected one of: {', '.join(sorted(SUPPORTED_SCHEMA_VERSIONS))}",
            )
        )


def _validate_month(row: int, record: dict[str, str], errors: list[ValidationError]) -> None:
    value = str(record.get("collection_month", "")).strip()
    if value and not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", value):
        errors.append(ValidationError(row, "collection_month", "expected YYYY-MM"))


def _validate_enums(row: int, record: dict[str, str], errors: list[ValidationError]) -> None:
    for field_name, allowed in ENUMS.items():
        value = str(record.get(field_name, "")).strip()
        if value and value not in allowed:
            errors.append(
                ValidationError(row, field_name, f"expected one of: {', '.join(sorted(allowed))}")
            )


def _validate_numbers(row: int, record: dict[str, str], errors: list[ValidationError]) -> None:
    for field_name, (minimum, maximum) in NUMERIC_RANGES.items():
        value = str(record.get(field_name, "")).strip()
        if not value:
            continue
        try:
            number = int(value)
        except ValueError:
            errors.append(ValidationError(row, field_name, "expected integer"))
            continue
        if number < minimum or number > maximum:
            errors.append(ValidationError(row, field_name, f"expected {minimum}-{maximum}"))

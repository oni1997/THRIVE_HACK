from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from typing import Iterable, Iterator


SCHEMA_VERSION = "0.1.0"
AGE_BANDS = ["10-14", "15-19", "20-24", "25-34", "35-44", "45-54"]
COUNTRIES = ["GH", "KE", "NG", "RW", "TZ", "UG", "ZA", "ZW"]
SETTINGS = ["urban", "peri_urban", "rural"]
FLOW = ["light", "moderate", "heavy", "very_heavy"]
YES_NO_UNKNOWN = ["yes", "no", "unknown"]
PRODUCT_ACCESS = ["reliable", "sometimes_limited", "often_limited", "unknown"]
CARE_ACCESS = ["visited_provider", "wanted_but_could_not_access", "not_needed", "unknown"]
METHODS = ["mobile_form", "paper_form", "chw_interview", "web_form"]
SYMPTOMS = [
    "cramps",
    "fatigue",
    "headache",
    "nausea",
    "dizziness",
    "mood_changes",
    "back_pain",
]

FIELDNAMES = [
    "schema_version",
    "record_id",
    "age_band",
    "country_code",
    "region",
    "setting",
    "collection_month",
    "cycle_length_days",
    "period_duration_days",
    "flow_heaviness",
    "pain_score",
    "reported_symptoms",
    "missed_school_or_work",
    "product_access",
    "healthcare_access",
    "collection_method",
    "source_type",
]


def generate_records(count: int, seed: int = 42, missingness: float = 0.0) -> list[dict[str, object]]:
    """Generate synthetic menstrual health records as a list."""
    return list(iter_records(count, seed=seed, missingness=missingness))


def iter_records(count: int, seed: int = 42, missingness: float = 0.0) -> Iterator[dict[str, object]]:
    """Yield synthetic menstrual health records for development and testing."""
    if count < 0:
        raise ValueError("count must be greater than or equal to 0")
    if missingness < 0 or missingness > 1:
        raise ValueError("missingness must be between 0 and 1")

    rng = random.Random(seed)
    for index in range(1, count + 1):
        symptom_count = rng.randint(0, 3)
        symptoms = sorted(rng.sample(SYMPTOMS, symptom_count))
        flow = rng.choice(FLOW)
        pain = _pain_score_for_flow(rng, flow)
        country = rng.choice(COUNTRIES)
        record = {
            "schema_version": SCHEMA_VERSION,
            "record_id": f"SYN-{index:05d}",
            "age_band": rng.choice(AGE_BANDS),
            "country_code": country,
            "region": synthetic_region(country, rng),
            "setting": rng.choice(SETTINGS),
            "collection_month": f"2026-{rng.randint(1, 12):02d}",
            "cycle_length_days": rng.randint(21, 35),
            "period_duration_days": rng.randint(2, 8),
            "flow_heaviness": flow,
            "pain_score": pain,
            "reported_symptoms": ";".join(symptoms),
            "missed_school_or_work": rng.choice(YES_NO_UNKNOWN),
            "product_access": rng.choice(PRODUCT_ACCESS),
            "healthcare_access": rng.choice(CARE_ACCESS),
            "collection_method": rng.choice(METHODS),
            "source_type": "synthetic",
        }
        _apply_optional_missingness(record, rng, missingness)
        yield record


def synthetic_region(country_code: str, rng: random.Random) -> str:
    """Return a coarse fictional region label, not a precise real location."""
    return f"{country_code}-region-{rng.randint(1, 4)}"


def write_csv(records: Iterable[dict[str, object]], output: str | Path) -> Path:
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in FIELDNAMES})
    return output_path


def write_jsonl(records: Iterable[dict[str, object]], output: str | Path) -> Path:
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    return output_path


def _pain_score_for_flow(rng: random.Random, flow: str) -> int:
    if flow in {"heavy", "very_heavy"}:
        return rng.randint(3, 10)
    return rng.randint(0, 7)


def _apply_optional_missingness(record: dict[str, object], rng: random.Random, missingness: float) -> None:
    for field in ("region", "reported_symptoms"):
        if rng.random() < missingness:
            record[field] = ""

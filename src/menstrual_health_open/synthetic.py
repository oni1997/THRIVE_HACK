from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from typing import Iterable, Iterator

from menstrual_health_open.conditions import (
    ALL_CONDITIONS,
    COAGULATION_DISORDER,
    FIBROIDS_ADENOMYOSIS,
    IRON_DEFICIENCY,
    ConditionProfile,
)


SCHEMA_VERSION = "0.1.0"
AGE_BANDS = ["10-14", "15-19", "20-24", "25-34", "35-44", "45-54"]
AGE_BAND_MIDPOINT = {"10-14": 12, "15-19": 17, "20-24": 22, "25-34": 30, "35-44": 40, "45-54": 50}
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

FREE_TEXT_TEMPLATES: dict[str, list[str]] = {
    "cramps": [
        "Really bad cramps this time, could barely stand",
        "Cramps started two days before my period",
        "Mild cramping on first day only",
        "Severe cramping that painkillers didn't help",
    ],
    "fatigue": [
        "Been feeling so tired I can't do my usual work",
        "Exhausted all through my period",
        "Low energy, sleeping more than usual",
        "Fatigue lasted for days after bleeding stopped",
    ],
    "heavy": [
        "Changing pads every hour on heavy days",
        "Bleeding through clothes twice this cycle",
        "Clots the size of coins passing",
        "Heavy flow that soaked through to my clothes",
    ],
    "back_pain": [
        "Lower back pain that radiates down my legs",
        "Back ache made it hard to sit through class",
        "Dull ache in my lower back the whole time",
    ],
    "dizziness": [
        "Felt lightheaded when standing up quickly",
        "Dizzy spells especially on heavy days",
        "Nearly fainted at the market",
    ],
}

CONDITION_FIELDNAMES = [
    "condition_iron_deficiency",
    "condition_fibroids",
    "condition_coagulation_disorder",
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
    "symptom_free_text",
    "missed_school_or_work",
    "product_access",
    "healthcare_access",
    "collection_method",
    "source_type",
    *CONDITION_FIELDNAMES,
]


def generate_records(count: int, seed: int = 42, missingness: float = 0.0,
                     include_conditions: bool = False) -> list[dict[str, object]]:
    return list(iter_records(count, seed=seed, missingness=missingness,
                             include_conditions=include_conditions))


def iter_records(count: int, seed: int = 42, missingness: float = 0.0,
                 include_conditions: bool = False) -> Iterator[dict[str, object]]:
    if count < 0:
        raise ValueError("count must be greater than or equal to 0")
    if missingness < 0 or missingness > 1:
        raise ValueError("missingness must be between 0 and 1")

    rng = random.Random(seed)
    for index in range(1, count + 1):
        age_band = rng.choice(AGE_BANDS)
        age_mid = AGE_BAND_MIDPOINT[age_band]
        country = rng.choice(COUNTRIES)
        setting = rng.choice(SETTINGS)

        has_iron_def = _roll_condition(rng, age_band, IRON_DEFICIENCY, 0.12)
        has_fibroids = _roll_condition(rng, age_band, FIBROIDS_ADENOMYOSIS, 0.08)
        has_coag = _roll_condition(rng, age_band, COAGULATION_DISORDER, 0.03)

        conditions = []
        if has_iron_def:
            conditions.append(IRON_DEFICIENCY)
        if has_fibroids:
            conditions.append(FIBROIDS_ADENOMYOSIS)
        if has_coag:
            conditions.append(COAGULATION_DISORDER)

        flow = _generate_flow(rng, conditions)
        pain = _generate_pain(rng, flow, conditions)
        cycle_len = _generate_cycle_length(rng, conditions)
        period_dur = _generate_period_duration(rng, conditions)
        symptoms = _generate_symptoms(rng, conditions)
        missed = _generate_missed(rng, conditions)
        free_text = _generate_free_text(rng, symptoms, flow)

        record = {
            "schema_version": SCHEMA_VERSION,
            "record_id": f"SYN-{index:05d}",
            "age_band": age_band,
            "country_code": country,
            "region": synthetic_region(country, rng),
            "setting": setting,
            "collection_month": f"2026-{rng.randint(1, 12):02d}",
            "cycle_length_days": cycle_len,
            "period_duration_days": period_dur,
            "flow_heaviness": flow,
            "pain_score": pain,
            "reported_symptoms": ";".join(sorted(symptoms)),
            "symptom_free_text": free_text if free_text and rng.random() < 0.6 else "",
            "missed_school_or_work": missed,
            "product_access": rng.choice(PRODUCT_ACCESS),
            "healthcare_access": rng.choice(CARE_ACCESS),
            "collection_method": rng.choice(METHODS),
            "source_type": "synthetic",
            "condition_iron_deficiency": "yes" if has_iron_def else "no",
            "condition_fibroids": "yes" if has_fibroids else "no",
            "condition_coagulation_disorder": "yes" if has_coag else "no",
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


def _roll_condition(rng: random.Random, age_band: str, profile: ConditionProfile, base_rate: float) -> bool:
    age_mult = profile.age_risk_bands.get(age_band, 1.0)
    probability = min(base_rate * age_mult, 0.5)
    return rng.random() < probability


def _generate_flow(rng: random.Random, conditions: list[ConditionProfile]) -> str:
    base = rng.choices(FLOW, weights=[25, 40, 25, 10])[0]
    if not conditions:
        return base
    bias = max(c.flow_weights.get("heavy", 0) for c in conditions)
    if rng.random() < bias * 0.6:
        return rng.choices(["heavy", "very_heavy"], weights=[60, 40])[0]
    return base


def _generate_pain(rng: random.Random, flow: str, conditions: list[ConditionProfile]) -> int:
    base = _pain_score_for_flow(rng, flow)
    if conditions:
        bonus = max(c.pain_threshold for c in conditions) * 0.15
        base = min(base + int(bonus), 10)
    return base


def _generate_cycle_length(rng: random.Random, conditions: list[ConditionProfile]) -> int:
    base = rng.randint(21, 35)
    if conditions:
        weights = [c.cycle_length_range for c in conditions]
        avg_min = sum(w[0] for w in weights) // len(weights)
        avg_max = sum(w[1] for w in weights) // len(weights)
        if rng.random() < 0.4:
            base = rng.randint(avg_min, avg_max)
    return max(15, min(base, 60))


def _generate_period_duration(rng: random.Random, conditions: list[ConditionProfile]) -> int:
    base = rng.randint(2, 8)
    if conditions:
        weights = [c.duration_range for c in conditions]
        avg_min = sum(w[0] for w in weights) // len(weights)
        avg_max = sum(w[1] for w in weights) // len(weights)
        if rng.random() < 0.5:
            base = rng.randint(avg_min, avg_max)
    return max(1, min(base, 14))


def _generate_symptoms(rng: random.Random, conditions: list[ConditionProfile]) -> list[str]:
    symptom_pool = set()
    base_count = rng.randint(0, 2)
    if base_count:
        symptom_pool.update(rng.sample(SYMPTOMS, base_count))
    for condition in conditions:
        for symptom, weight in condition.symptom_weights.items():
            if rng.random() < weight * 0.7:
                symptom_pool.add(symptom)
        if rng.random() < 0.6:
            symptom_pool.add(rng.choice(condition.key_symptoms))
    return list(symptom_pool)


def _generate_missed(rng: random.Random, conditions: list[ConditionProfile]) -> str:
    if not conditions:
        return rng.choice(YES_NO_UNKNOWN)
    prob_yes = max(c.missed_work_weight for c in conditions)
    if rng.random() < prob_yes:
        return "yes"
    if rng.random() < 0.3:
        return "unknown"
    return "no"


def _generate_free_text(rng: random.Random, symptoms: list[str], flow: str) -> str:
    parts = []
    for symptom in symptoms:
        if symptom in FREE_TEXT_TEMPLATES and rng.random() < 0.4:
            parts.append(rng.choice(FREE_TEXT_TEMPLATES[symptom]))
    if flow in {"heavy", "very_heavy"} and rng.random() < 0.3:
        parts.append(rng.choice(FREE_TEXT_TEMPLATES["heavy"]))
    return " | ".join(parts) if parts else ""


def _pain_score_for_flow(rng: random.Random, flow: str) -> int:
    if flow in {"heavy", "very_heavy"}:
        return rng.randint(3, 10)
    return rng.randint(0, 7)


def _apply_optional_missingness(record: dict[str, object], rng: random.Random, missingness: float) -> None:
    for field in ("region", "reported_symptoms"):
        if rng.random() < missingness:
            record[field] = ""

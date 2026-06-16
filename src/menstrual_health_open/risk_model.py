from __future__ import annotations

from typing import Any

from menstrual_health_open.conditions import (
    ALL_CONDITIONS,
    CONDITION_BY_NAME,
    ConditionProfile,
)


SYMPTOM_FIELD = "reported_symptoms"
FLOW_ORDER = {"light": 0, "moderate": 1, "heavy": 2, "very_heavy": 3}
AGE_BAND_ORDER = {"10-14": 0, "15-19": 1, "20-24": 2, "25-34": 3, "35-44": 4, "45-54": 5}


def parse_symptoms(record: dict[str, Any]) -> list[str]:
    raw = str(record.get(SYMPTOM_FIELD, "")).strip()
    return [s.strip() for s in raw.split(";") if s.strip()]


def score_condition(record: dict[str, Any], profile: ConditionProfile) -> float:
    age_band = str(record.get("age_band", ""))
    flow = str(record.get("flow_heaviness", ""))
    pain = _int_or(record.get("pain_score"), 0)
    cycle_len = _int_or(record.get("cycle_length_days"), 28)
    period_dur = _int_or(record.get("period_duration_days"), 5)
    missed = str(record.get("missed_school_or_work", ""))
    symptoms = parse_symptoms(record)

    score = 0.0
    max_score = 0.0

    age_weight = profile.age_risk_bands.get(age_band, 1.0)
    score += age_weight * 10
    max_score += 15

    flow_w = profile.flow_weights.get(flow, 0.3)
    score += flow_w * 20
    max_score += 20

    if pain >= profile.pain_threshold:
        score += 10
    score += min(pain / 10.0, 1.0) * 5
    max_score += 15

    if cycle_len < profile.cycle_length_range[1]:
        score += 5
    if period_dur > profile.duration_range[0]:
        score += 5
    max_score += 10

    if missed == "yes":
        score += profile.missed_work_weight * 10
    max_score += 10

    symptom_matches = sum(profile.symptom_weights.get(s, 0) for s in symptoms)
    score += symptom_matches * 5
    max_score += 20

    key_matches = sum(1 for s in symptoms if s in profile.key_symptoms)
    score += key_matches * 5
    max_score += 10

    return round((score / max_score) * 100, 1) if max_score > 0 else 0.0


def score_all_conditions(record: dict[str, Any]) -> dict[str, float]:
    return {c.name: score_condition(record, c) for c in ALL_CONDITIONS}


def top_condition(record: dict[str, Any]) -> tuple[str, float]:
    scores = score_all_conditions(record)
    best = max(scores, key=scores.get)
    return best, scores[best]


def risk_level(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "moderate"
    return "low"


def _int_or(value: object, default: int) -> int:
    try:
        return int(str(value))
    except (ValueError, TypeError):
        return default

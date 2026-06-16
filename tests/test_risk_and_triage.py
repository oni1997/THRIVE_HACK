from __future__ import annotations

from menstrual_health_open.risk_model import (
    parse_symptoms,
    score_condition,
    score_all_conditions,
    risk_level,
)
from menstrual_health_open.triage import triage_record, triage_summary
from menstrual_health_open.conditions import IRON_DEFICIENCY, FIBROIDS_ADENOMYOSIS
from menstrual_health_open.synthetic import iter_records


def _make_record(**overrides: object) -> dict[str, object]:
    base = {
        "age_band": "25-34",
        "flow_heaviness": "heavy",
        "pain_score": "6",
        "cycle_length_days": "25",
        "period_duration_days": "7",
        "missed_school_or_work": "yes",
        "reported_symptoms": "fatigue;dizziness;cramps",
    }
    base.update(overrides)
    return base


class TestParseSymptoms:
    def test_parses_semicolon_separated(self) -> None:
        assert parse_symptoms({"reported_symptoms": "cramps;fatigue"}) == ["cramps", "fatigue"]

    def test_handles_empty(self) -> None:
        assert parse_symptoms({"reported_symptoms": ""}) == []

    def test_handles_missing_key(self) -> None:
        assert parse_symptoms({}) == []


class TestScoreCondition:
    def test_high_risk_iron_deficiency(self) -> None:
        record = _make_record(
            flow_heaviness="very_heavy",
            pain_score="8",
            reported_symptoms="fatigue;dizziness",
        )
        score = score_condition(record, IRON_DEFICIENCY)
        assert score >= 50, f"Expected high risk, got {score}"

    def test_low_risk_young_fibroids(self) -> None:
        record = _make_record(
            age_band="10-14",
            flow_heaviness="light",
            pain_score="1",
            reported_symptoms="",
            missed_school_or_work="unknown",
            cycle_length_days="30",
            period_duration_days="3",
        )
        score = score_condition(record, FIBROIDS_ADENOMYOSIS)
        assert score < 50, f"Expected low risk, got {score}"

    def test_all_conditions_return_scores(self) -> None:
        record = _make_record()
        scores = score_all_conditions(record)
        assert len(scores) == 3
        for name, score in scores.items():
            assert 0 <= score <= 100, f"{name}: {score} out of range"

    def test_always_returns_top_condition(self) -> None:
        record = _make_record(
            flow_heaviness="very_heavy",
            reported_symptoms="fatigue;dizziness",
        )
        scores = score_all_conditions(record)
        top = max(scores, key=scores.get)
        assert top in scores


class TestRiskLevel:
    def test_high(self) -> None:
        assert risk_level(85) == "high"

    def test_moderate(self) -> None:
        assert risk_level(55) == "moderate"

    def test_low(self) -> None:
        assert risk_level(20) == "low"


class TestTriage:
    def test_triage_record_returns_sorted_results(self) -> None:
        record = _make_record()
        results = triage_record(record)
        assert len(results) == 3
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_triage_summary_contains_primary(self) -> None:
        record = _make_record()
        summary = triage_summary(record)
        assert "PRIMARY CONCERN" in summary
        assert "RECOMMENDED ACTION" in summary

    def test_triage_on_synthetic_record(self) -> None:
        records = list(iter_records(5, seed=42))
        for record in records:
            results = triage_record(record)
            assert len(results) == 3
            top = results[0]
            assert top.score >= 0
            assert top.risk in ("low", "moderate", "high")

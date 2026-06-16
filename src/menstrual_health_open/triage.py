from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from menstrual_health_open.conditions import ALL_CONDITIONS
from menstrual_health_open.risk_model import risk_level, score_condition


@dataclass
class TriageResult:
    condition: str
    score: float
    risk: str
    label: str
    referral: str
    key_factors: list[str]


def triage_record(record: dict[str, Any]) -> list[TriageResult]:
    results = []
    for profile in ALL_CONDITIONS:
        s = score_condition(record, profile)
        key_factors = _extract_key_factors(record, profile)
        results.append(TriageResult(
            condition=profile.name,
            score=s,
            risk=risk_level(s),
            label=profile.label,
            referral=profile.referral_advice,
            key_factors=key_factors,
        ))
    results.sort(key=lambda r: r.score, reverse=True)
    return results


def triage_summary(record: dict[str, Any]) -> str:
    results = triage_record(record)
    lines = [">>> CHW Triage Report", f"   Patient: {record.get('record_id', 'N/A')}", ""]
    for r in results:
        marker = "*" if r.risk == "high" else "+" if r.risk == "moderate" else " "
        lines.append(f"  [{marker}] {r.label}: {r.score:.0f}/100 ({r.risk.upper()})")
        for f in r.key_factors[:3]:
            lines.append(f"       - {f}")
        if r.risk in ("high", "moderate"):
            lines.append(f"       >> {r.referral}")
        lines.append("")
    top = results[0]
    lines.append(f"  PRIMARY CONCERN: {top.label} (score: {top.score:.0f}/100, {top.risk} risk)")
    lines.append(f"  RECOMMENDED ACTION: {top.referral}")
    return "\n".join(lines)


def _extract_key_factors(record: dict[str, Any], profile) -> list[str]:
    factors = []
    age = str(record.get("age_band", ""))
    flow = str(record.get("flow_heaviness", ""))
    pain = str(record.get("pain_score", "0"))
    missed = str(record.get("missed_school_or_work", ""))
    symptoms = str(record.get("reported_symptoms", ""))

    age_w = profile.age_risk_bands.get(age, 1.0)
    if age_w > 1.2:
        factors.append(f"Age group {age} has elevated risk for {profile.label.lower()}")
    elif age_w < 0.5:
        factors.append(f"Age group {age} has lower typical risk for {profile.label.lower()}")

    flow_w = profile.flow_weights.get(flow, 0)
    if flow_w >= 0.8:
        factors.append(f"Flow heaviness '{flow}' matches condition profile")
    if int(pain) >= profile.pain_threshold:
        factors.append(f"Pain score ({pain}) exceeds threshold of {profile.pain_threshold}")
    if missed == "yes":
        factors.append("Missed school/work due to symptoms")
    sym_list = [s.strip() for s in symptoms.split(";") if s.strip()]
    matches = [s for s in sym_list if s in profile.symptom_weights and profile.symptom_weights[s] >= 0.5]
    if matches:
        factors.append(f"Key symptoms present: {', '.join(matches)}")
    return factors

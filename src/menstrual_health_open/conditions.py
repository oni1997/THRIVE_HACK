from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


ConditionName = Literal["iron_deficiency", "fibroids_adenomyosis", "coagulation_disorder"]


@dataclass(frozen=True)
class ConditionProfile:
    name: str
    label: str
    description: str
    key_symptoms: list[str]
    age_risk_bands: dict[str, float]
    flow_weights: dict[str, float]
    pain_threshold: int
    cycle_length_range: tuple[int, int]
    duration_range: tuple[int, int]
    missed_work_weight: float
    symptom_weights: dict[str, float]
    referral_advice: str


IRON_DEFICIENCY = ConditionProfile(
    name="iron_deficiency",
    label="Iron Deficiency / Anaemia",
    description="Caused by heavy menstrual blood loss depleting iron stores. "
    "Common in women with heavy bleeding, especially in low-resource settings with limited nutrition.",
    key_symptoms=["fatigue", "dizziness", "headache"],
    age_risk_bands={
        "10-14": 0.6,
        "15-19": 1.2,
        "20-24": 1.3,
        "25-34": 1.5,
        "35-44": 1.2,
        "45-54": 0.8,
    },
    flow_weights={"light": 0.3, "moderate": 0.5, "heavy": 0.8, "very_heavy": 1.0},
    pain_threshold=4,
    cycle_length_range=(18, 28),
    duration_range=(5, 10),
    missed_work_weight=0.4,
    symptom_weights={
        "fatigue": 1.0,
        "dizziness": 0.9,
        "headache": 0.5,
        "cramps": 0.2,
        "nausea": 0.3,
        "mood_changes": 0.3,
        "back_pain": 0.1,
    },
    referral_advice="Refer for haemoglobin test and iron supplementation. "
    "If Hb < 8 g/dL or signs of severe anaemia, refer urgently.",
)


FIBROIDS_ADENOMYOSIS = ConditionProfile(
    name="fibroids_adenomyosis",
    label="Fibroids / Adenomyosis",
    description="Structural uterine conditions causing heavy bleeding and severe pain. "
    "More common in women aged 30-50. Can cause significant quality-of-life impairment.",
    key_symptoms=["cramps", "back_pain", "mood_changes"],
    age_risk_bands={
        "10-14": 0.1,
        "15-19": 0.3,
        "20-24": 0.6,
        "25-34": 1.2,
        "35-44": 1.8,
        "45-54": 1.5,
    },
    flow_weights={"light": 0.2, "moderate": 0.4, "heavy": 0.8, "very_heavy": 1.0},
    pain_threshold=6,
    cycle_length_range=(21, 35),
    duration_range=(5, 14),
    missed_work_weight=0.6,
    symptom_weights={
        "cramps": 1.0,
        "back_pain": 0.8,
        "mood_changes": 0.5,
        "fatigue": 0.5,
        "nausea": 0.4,
        "dizziness": 0.2,
        "headache": 0.2,
    },
    referral_advice="Refer for pelvic ultrasound. If pain is severe or bleeding is "
    "heavy enough to cause anaemia, refer to gynaecology.",
)


COAGULATION_DISORDER = ConditionProfile(
    name="coagulation_disorder",
    label="Coagulation Disorder",
    description="Bleeding disorders such as von Willebrand disease that cause "
    "prolonged or excessive bleeding. Often underdiagnosed in women with lifelong heavy periods.",
    key_symptoms=["dizziness", "fatigue"],
    age_risk_bands={
        "10-14": 1.5,
        "15-19": 1.3,
        "20-24": 1.1,
        "25-34": 0.9,
        "35-44": 0.6,
        "45-54": 0.4,
    },
    flow_weights={"light": 0.1, "moderate": 0.3, "heavy": 0.8, "very_heavy": 1.0},
    pain_threshold=3,
    cycle_length_range=(15, 25),
    duration_range=(7, 14),
    missed_work_weight=0.7,
    symptom_weights={
        "dizziness": 0.9,
        "fatigue": 0.8,
        "cramps": 0.3,
        "nausea": 0.3,
        "headache": 0.3,
        "mood_changes": 0.2,
        "back_pain": 0.2,
    },
    referral_advice="Refer for coagulation screen (PT, aPTT, von Willebrand panel). "
    "If bleeding is severe or patient is haemodynamically unstable, refer urgently.",
)


ALL_CONDITIONS: list[ConditionProfile] = [
    IRON_DEFICIENCY,
    FIBROIDS_ADENOMYOSIS,
    COAGULATION_DISORDER,
]


CONDITION_BY_NAME: dict[str, ConditionProfile] = {c.name: c for c in ALL_CONDITIONS}

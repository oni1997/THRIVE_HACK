from __future__ import annotations

from menstrual_health_open.synthetic import generate_records, iter_records, write_csv
from menstrual_health_open.validation import validate_file


def test_synthetic_records_validate(tmp_path):
    records = generate_records(10, seed=7)
    output = tmp_path / "records.csv"
    write_csv(records, output)

    report = validate_file(output)

    assert report.valid
    assert report.row_count == 10
    assert report.completeness_score == 1.0


def test_iter_records_streams_records():
    records = iter_records(2, seed=7)

    first = next(records)
    second = next(records)

    assert first["record_id"] == "SYN-00001"
    assert second["record_id"] == "SYN-00002"


def test_validation_flags_missing_required_field(tmp_path):
    output = tmp_path / "bad.csv"
    output.write_text(
        "schema_version,record_id,age_band,country_code,setting,collection_month,cycle_length_days,"
        "period_duration_days,flow_heaviness,pain_score,missed_school_or_work,"
        "product_access,healthcare_access,collection_method,source_type\n"
        "0.1.0,SYN-1,15-19,ZW,rural,2026-01,28,5,heavy,,yes,reliable,not_needed,web_form,synthetic\n",
        encoding="utf-8",
    )

    report = validate_file(output)

    assert not report.valid
    assert any(error.field == "pain_score" for error in report.errors)

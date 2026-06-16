from __future__ import annotations

import sys
from pathlib import Path

# Ensure the core package is importable on Streamlit Cloud
_src = Path(__file__).resolve().parents[1] / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

import altair as alt
import pandas as pd
import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = REPO_ROOT / "synthetic-data" / "datasets" / "survey_responses_1000.csv"

AGE_BAND_ORDER = ["10-14", "15-19", "20-24", "25-34", "35-44", "45-54"]
FLOW_ORDER = ["light", "moderate", "heavy", "very_heavy"]

st.set_page_config(page_title="Menstrual Health Open — Starter Dashboard", layout="wide")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["reported_symptoms"] = df["reported_symptoms"].fillna("")
    return df


def render_explore_tab(df: pd.DataFrame) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Records", f"{len(df):,}")
    col2.metric("Median cycle length", f"{df['cycle_length_days'].median():.0f} days")
    col3.metric("Median pain score", f"{df['pain_score'].median():.0f} / 10")
    missed = (df["missed_school_or_work"] == "yes").mean()
    col4.metric("Missed school/work", f"{missed:.0%}")

    left, right = st.columns(2)

    with left:
        st.subheader("Pain score by flow heaviness")
        pain_chart = (
            alt.Chart(df)
            .mark_boxplot()
            .encode(
                x=alt.X("flow_heaviness:N", sort=FLOW_ORDER, title="Flow heaviness"),
                y=alt.Y("pain_score:Q", title="Pain score (0-10)"),
                color=alt.Color("flow_heaviness:N", sort=FLOW_ORDER, legend=None),
            )
        )
        st.altair_chart(pain_chart, use_container_width=True)

        st.subheader("Cycle length distribution")
        cycle_chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("cycle_length_days:Q", bin=alt.Bin(step=1), title="Cycle length (days)"),
                y=alt.Y("count()", title="Records"),
            )
        )
        st.altair_chart(cycle_chart, use_container_width=True)

    with right:
        st.subheader("Reported symptoms")
        symptoms = (
            df["reported_symptoms"]
            .str.split(";")
            .explode()
            .str.strip()
        )
        symptoms = symptoms[symptoms != ""]
        symptom_counts = symptoms.value_counts().reset_index()
        symptom_counts.columns = ["symptom", "count"]
        symptom_chart = (
            alt.Chart(symptom_counts)
            .mark_bar()
            .encode(
                x=alt.X("count:Q", title="Records"),
                y=alt.Y("symptom:N", sort="-x", title="Symptom"),
            )
        )
        st.altair_chart(symptom_chart, use_container_width=True)

        st.subheader("Product access by setting")
        access_chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("setting:N", title="Setting"),
                y=alt.Y("count()", stack="normalize", title="Share of records"),
                color=alt.Color("product_access:N", title="Product access"),
            )
        )
        st.altair_chart(access_chart, use_container_width=True)

    st.subheader("Records by collection month")
    month_chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("collection_month:N", title="Collection month"),
            y=alt.Y("count()", title="Records"),
        )
    )
    st.altair_chart(month_chart, use_container_width=True)

    with st.expander("Browse filtered records"):
        st.dataframe(df, use_container_width=True)


def render_triage_tab(df: pd.DataFrame) -> None:
    from menstrual_health_open.triage import triage_record

    st.subheader("CHW Triage Tool")
    st.caption(
        "Runs a symptom-based risk assessment on each record. "
        "Scores are computed from self-reported data alone — no lab results required. "
        "This is a decision-support tool, not a clinical diagnosis."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**Select a record to triage**")
        record_ids = df["record_id"].tolist()
        selected_id = st.selectbox("Record ID", record_ids, label_visibility="collapsed")
        record = df[df["record_id"] == selected_id].iloc[0].to_dict()

        st.markdown("**Patient profile**")
        st.markdown(f"- Age band: {record['age_band']}")
        st.markdown(f"- Setting: {record['setting']}")
        st.markdown(f"- Flow: {record['flow_heaviness']}")
        st.markdown(f"- Pain: {record['pain_score']}/10")
        st.markdown(f"- Cycle: {record['cycle_length_days']} days")
        st.markdown(f"- Period: {record['period_duration_days']} days")
        st.markdown(f"- Missed school/work: {record['missed_school_or_work']}")
        symptoms = str(record.get("reported_symptoms", ""))
        if symptoms:
            st.markdown(f"- Symptoms: {symptoms}")
        free_text = str(record.get("symptom_free_text", ""))
        if free_text:
            st.markdown(f"- Self-report: *{free_text}*")

    with col2:
        results = triage_record(record)
        for r in results:
            color = "red" if r.risk == "high" else "orange" if r.risk == "moderate" else "green"
            st.markdown(
                f"<h4 style='color:{color};'>{'⚠️' if r.risk != 'low' else '✓'} "
                f"{r.label}: {r.score:.0f}/100 ({r.risk.upper()})</h4>",
                unsafe_allow_html=True,
            )
            if r.key_factors:
                for f in r.key_factors:
                    st.markdown(f"- {f}")
            if r.risk in ("high", "moderate"):
                st.warning(r.referral)
                st.markdown("---")

    st.subheader("Cohort risk overview")
    risk_data = []
    for _, row in df.iterrows():
        results = triage_record(row.to_dict())
        risk_data.append({r.condition: r.score for r in results})
    risk_df = pd.DataFrame(risk_data)
    risk_df["record_id"] = df["record_id"].values

    risk_long = risk_df.melt(
        id_vars=["record_id"],
        var_name="condition",
        value_name="score",
    )
    condition_labels = {
        "iron_deficiency": "Iron Deficiency",
        "fibroids_adenomyosis": "Fibroids / Adenomyosis",
        "coagulation_disorder": "Coagulation Disorder",
    }
    risk_long["label"] = risk_long["condition"].map(condition_labels)

    chart = (
        alt.Chart(risk_long)
        .mark_boxplot()
        .encode(
            x=alt.X("label:N", title="Condition", sort=list(condition_labels.values())),
            y=alt.Y("score:Q", title="Risk score (0-100)"),
            color=alt.Color("label:N", legend=None),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    if "condition_iron_deficiency" in df.columns:
        st.subheader("Model accuracy vs ground truth")
        actual = df["condition_iron_deficiency"].eq("yes").astype(int)
        predicted = (risk_df["iron_deficiency"] >= 50).astype(int)
        correct = (actual == predicted).sum()
        st.metric("Iron deficiency prediction accuracy", f"{correct / len(df):.0%}")
        st.caption("Ground truth labels are synthetic and do not reflect real prevalence.")


def main() -> None:
    st.title("Menstrual Health Open — Starter Dashboard")
    st.caption(
        "All data shown is synthetic. Distributions are simulated and do not "
        "represent real prevalence. Build on this template with synthetic or "
        "reviewed aggregate data only."
    )

    uploaded = st.sidebar.file_uploader("Load a dataset (CSV)", type="csv")
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        df["reported_symptoms"] = df["reported_symptoms"].fillna("")
    else:
        df = load_data(DEFAULT_DATASET)

    st.sidebar.header("Filters")
    countries = st.sidebar.multiselect(
        "Country", sorted(df["country_code"].unique()), default=sorted(df["country_code"].unique())
    )
    age_bands = st.sidebar.multiselect(
        "Age band", AGE_BAND_ORDER, default=AGE_BAND_ORDER
    )
    settings = st.sidebar.multiselect(
        "Setting", sorted(df["setting"].unique()), default=sorted(df["setting"].unique())
    )

    filtered = df[
        df["country_code"].isin(countries)
        & df["age_band"].isin(age_bands)
        & df["setting"].isin(settings)
    ]

    if filtered.empty:
        st.warning("No records match the current filters.")
        return

    tab1, tab2 = st.tabs(["Explore Data", "CHW Triage Tool"])

    with tab1:
        render_explore_tab(filtered)

    with tab2:
        render_triage_tab(filtered)


if __name__ == "__main__":
    main()

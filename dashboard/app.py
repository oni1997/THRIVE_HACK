"""Starter dashboard for synthetic menstrual health data.

Run from the repository root:

    pip install -r dashboard/requirements.txt
    streamlit run dashboard/app.py

This dashboard reads bundled synthetic data only. Public dashboards built on
this template must use synthetic or reviewed aggregate data — never real
participant-level records. See governance/ for the rules.
"""
from __future__ import annotations

from pathlib import Path

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

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Records", f"{len(filtered):,}")
    col2.metric("Median cycle length", f"{filtered['cycle_length_days'].median():.0f} days")
    col3.metric("Median pain score", f"{filtered['pain_score'].median():.0f} / 10")
    missed = (filtered["missed_school_or_work"] == "yes").mean()
    col4.metric("Missed school/work", f"{missed:.0%}")

    left, right = st.columns(2)

    with left:
        st.subheader("Pain score by flow heaviness")
        pain_chart = (
            alt.Chart(filtered)
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
            alt.Chart(filtered)
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
            filtered["reported_symptoms"]
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
            alt.Chart(filtered)
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
        alt.Chart(filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("collection_month:N", title="Collection month"),
            y=alt.Y("count()", title="Records"),
        )
    )
    st.altair_chart(month_chart, use_container_width=True)

    with st.expander("Browse filtered records"):
        st.dataframe(filtered, use_container_width=True)


if __name__ == "__main__":
    main()

from __future__ import annotations

import sys
from pathlib import Path

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

st.set_page_config(page_title="THRIVE Triage — Menstrual Health Decision Support", layout="wide")

alt.themes.register("thrive", lambda: {
    "config": {
        "view": {"stroke": "transparent"},
        "axis": {"labelFontSize": 12, "titleFontSize": 13, "grid": False},
        "header": {"labelFontSize": 12, "titleFontSize": 13},
        "legend": {"labelFontSize": 11},
        "range": {
            "category": ["#006D77", "#E29578", "#2A9D8F", "#FFB703", "#264653", "#8AB17D"],
            "diverging": ["#D62828", "#FFB703", "#2A9D8F"],
            "heatmap": ["#006D77", "#83C5BE", "#E8E8E4"],
        },
    }
})
alt.themes.enable("thrive")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    .stApp { background: #FAF9F6; }
    h1, h2, h3 { color: #1A1A2E !important; font-weight: 600 !important; }
    .stMetric label { color: #006D77 !important; font-weight: 600 !important; }
    .stMetric [data-testid="stMetricValue"] { color: #1A1A2E !important; font-weight: 700 !important; }
    .risk-high { background: #FEF1F0; border-left: 4px solid #D62828; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; }
    .risk-moderate { background: #FFF8E7; border-left: 4px solid #FFB703; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; }
    .risk-low { background: #F0F9F6; border-left: 4px solid #2A9D8F; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; }
    .risk-badge-high { background: #D62828; color: white; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }
    .risk-badge-moderate { background: #FFB703; color: #1A1A2E; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }
    .risk-badge-low { background: #2A9D8F; color: white; padding: 0.15rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }
    .patient-card { background: white; border: 1px solid #E8E8E4; border-radius: 0.75rem; padding: 1.25rem; }
    .referral-box { background: #FFF8E7; border: 1px solid #FFB703; border-radius: 0.5rem; padding: 0.75rem; margin-top: 0.5rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { border-radius: 0.5rem 0.5rem 0 0; padding: 0.5rem 1rem; font-weight: 500; }
    .stTabs [aria-selected="true"] { background: #006D77 !important; color: white !important; }
    footer { text-align: center; color: #888; font-size: 0.8rem; padding-top: 2rem; }
    @media (max-width: 768px) { .row-widget.stColumns { flex-direction: column; } }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["reported_symptoms"] = df["reported_symptoms"].fillna("")
    return df


def metric_card(label: str, value: str, delta: str | None = None) -> None:
    st.markdown(f"""
    <div style="background:white;border:1px solid #E8E8E4;border-radius:0.75rem;padding:1rem;text-align:center;">
        <div style="color:#006D77;font-size:0.85rem;font-weight:600;">{label}</div>
        <div style="color:#1A1A2E;font-size:1.75rem;font-weight:700;line-height:1.2;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_explore_tab(df: pd.DataFrame) -> None:
    cols = st.columns(4)
    for c, (label, value) in zip(cols, [
        ("Records", f"{len(df):,}"),
        ("Median cycle", f"{df['cycle_length_days'].median():.0f} days"),
        ("Median pain", f"{df['pain_score'].median():.0f} / 10"),
        ("Missed school/work", f"{(df['missed_school_or_work'] == 'yes').mean():.0%}"),
    ]):
        with c:
            metric_card(label, value)

    left, right = st.columns(2)

    with left:
        st.subheader("Pain score by flow heaviness")
        st.altair_chart(
            alt.Chart(df).mark_boxplot().encode(
                x=alt.X("flow_heaviness:N", sort=FLOW_ORDER, title=None),
                y=alt.Y("pain_score:Q", title="Pain score (0-10)"),
                color=alt.Color("flow_heaviness:N", sort=FLOW_ORDER, legend=None,
                                scale=alt.Scale(range=["#83C5BE", "#006D77", "#E29578", "#D62828"])),
            ).properties(height=250),
            use_container_width=True,
        )

        st.subheader("Cycle length distribution")
        st.altair_chart(
            alt.Chart(df).mark_bar(color="#006D77", opacity=0.85).encode(
                x=alt.X("cycle_length_days:Q", bin=alt.Bin(step=1), title="Cycle length (days)"),
                y=alt.Y("count()", title="Records"),
            ).properties(height=200),
            use_container_width=True,
        )

    with right:
        st.subheader("Reported symptoms")
        symptoms = df["reported_symptoms"].str.split(";").explode().str.strip()
        symptoms = symptoms[symptoms != ""]
        symptom_counts = symptoms.value_counts().reset_index()
        symptom_counts.columns = ["symptom", "count"]
        st.altair_chart(
            alt.Chart(symptom_counts).mark_bar(color="#E29578", opacity=0.85).encode(
                x=alt.X("count:Q", title="Records"),
                y=alt.Y("symptom:N", sort="-x", title=None),
            ).properties(height=250),
            use_container_width=True,
        )

        st.subheader("Product access by setting")
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(
                x=alt.X("setting:N", title=None),
                y=alt.Y("count()", stack="normalize", title="Share"),
                color=alt.Color("product_access:N", title="Access",
                                scale=alt.Scale(range=["#006D77", "#83C5BE", "#E29578", "#264653"])),
            ).properties(height=200),
            use_container_width=True,
        )

    st.subheader("Records over time")
    st.altair_chart(
        alt.Chart(df).mark_line(point=True, color="#006D77", strokeWidth=2).encode(
            x=alt.X("collection_month:N", title="Month"),
            y=alt.Y("count()", title="Records"),
        ).properties(height=250),
        use_container_width=True,
    )

    with st.expander("Browse filtered records"):
        st.dataframe(df, use_container_width=True, hide_index=True)


def render_triage_tab(df: pd.DataFrame) -> None:
    from menstrual_health_open.triage import triage_record

    st.markdown(
        "<p style='color:#666;margin-top:-0.5rem;'>"
        "Symptom-based risk assessment using self-reported data only — "
        "no labs, no imaging, no internet. "
        "<strong>Decision-support only, not a clinical diagnosis.</strong></p>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1.6])

    with left:
        record_ids = df["record_id"].tolist()
        selected_id = st.selectbox("Select patient", record_ids, label_visibility="collapsed",
                                   placeholder="Choose a record...")
        record = df[df["record_id"] == selected_id].iloc[0].to_dict()

        st.markdown("<div class='patient-card'>", unsafe_allow_html=True)
        st.markdown(f"**{selected_id}**")
        cols = st.columns(2)
        cols[0].markdown(f"Age: **{record['age_band']}**")
        cols[1].markdown(f"Setting: **{record['setting']}**")
        cols[0].markdown(f"Flow: **{record['flow_heaviness']}**")
        cols[1].markdown(f"Pain: **{record['pain_score']}** / 10")
        cols[0].markdown(f"Cycle: **{record['cycle_length_days']}** days")
        cols[1].markdown(f"Period: **{record['period_duration_days']}** days")
        st.markdown(f"Missed school/work: **{record['missed_school_or_work']}**")
        symptoms = str(record.get("reported_symptoms", ""))
        if symptoms:
            st.markdown(f"Symptoms: **{symptoms}**")
        free_text = str(record.get("symptom_free_text", ""))
        if free_text:
            st.markdown(f"<em>“{free_text}”</em>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        results = triage_record(record)
        for r in results:
            cls = f"risk-{r.risk}"
            badge = f"<span class='risk-badge-{r.risk}'>{r.risk.upper()}</span>"
            icon = "⚠️" if r.risk == "high" else "⚡" if r.risk == "moderate" else "✓"
            st.markdown(
                f"<div class='{cls}'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
                f"<strong>{icon} {r.label}</strong>"
                f"<span><strong>{r.score:.0f}</strong>/100 {badge}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if r.key_factors:
                for f in r.key_factors[:3]:
                    st.markdown(f"- {f}")
            if r.risk in ("high", "moderate"):
                st.markdown(
                    f"<div class='referral-box'><strong>Referral:</strong> {r.referral}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)
    st.subheader("Cohort risk distribution")

    risk_data = []
    for _, row in df.iterrows():
        scores = {r.condition: r.score for r in triage_record(row.to_dict())}
        scores["record_id"] = row["record_id"]
        risk_data.append(scores)
    risk_df = pd.DataFrame(risk_data)

    risk_long = risk_df.melt(id_vars=["record_id"], var_name="condition", value_name="score")
    condition_labels = {
        "iron_deficiency": "Iron Deficiency",
        "fibroids_adenomyosis": "Fibroids / Adenomyosis",
        "coagulation_disorder": "Coagulation Disorder",
    }
    risk_long["label"] = risk_long["condition"].map(condition_labels)

    st.altair_chart(
        alt.Chart(risk_long).mark_boxplot().encode(
            x=alt.X("label:N", title=None, sort=list(condition_labels.values())),
            y=alt.Y("score:Q", title="Risk score (0-100)", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color("label:N", legend=None,
                            scale=alt.Scale(domain=list(condition_labels.values()),
                                            range=["#006D77", "#E29578", "#2A9D8F"])),
        ).properties(height=280),
        use_container_width=True,
    )

    if "condition_iron_deficiency" in df.columns:
        col_a, col_b, col_c = st.columns(3)
        for col, cond, label in [
            (col_a, "condition_iron_deficiency", "Iron Deficiency"),
            (col_b, "condition_fibroids", "Fibroids / Adenomyosis"),
            (col_c, "condition_coagulation_disorder", "Coagulation Disorder"),
        ]:
            with col:
                actual = df[cond].eq("yes").astype(int)
                cond_key = cond.replace("condition_", "").replace("_", "_")
                if cond_key == "fibroids":
                    cond_key = "fibroids_adenomyosis"
                predicted = (risk_df[cond_key] >= 50).astype(int)
                correct = (actual == predicted).sum()
                metric_card(f"{label} accuracy", f"{correct / len(df):.0%}")

        st.caption("Ground truth labels are synthetic — accuracy reflects the rule-based model against generated labels, not real clinical performance.")

    st.markdown("<footer>THRIVE Hackathon 2026 · FlameLily Foundation · Mavara Research Collective</footer>",
                unsafe_allow_html=True)


def main() -> None:
    st.title("THRIVE Triage")
    st.markdown(
        "<p style='color:#666;margin-top:-0.75rem;margin-bottom:1.5rem;'>"
        "Menstrual health decision-support · "
        "<em>All data shown is synthetic — distributions are simulated.</em></p>",
        unsafe_allow_html=True,
    )

    uploaded = st.sidebar.file_uploader("Load data (CSV)", type="csv")
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        df["reported_symptoms"] = df["reported_symptoms"].fillna("")
    else:
        df = load_data(DEFAULT_DATASET)

    st.sidebar.markdown("---")
    st.sidebar.header("Filters")
    countries = st.sidebar.multiselect(
        "Country", sorted(df["country_code"].unique()),
        default=sorted(df["country_code"].unique()),
        placeholder="All countries",
    )
    age_bands = st.sidebar.multiselect(
        "Age band", AGE_BAND_ORDER, default=AGE_BAND_ORDER, placeholder="All ages",
    )
    settings = st.sidebar.multiselect(
        "Setting", sorted(df["setting"].unique()),
        default=sorted(df["setting"].unique()),
        placeholder="All settings",
    )

    filtered = df[
        df["country_code"].isin(countries)
        & df["age_band"].isin(age_bands)
        & df["setting"].isin(settings)
    ]

    if filtered.empty:
        st.warning("No records match the current filters. Adjust your selection.")
        return

    tab1, tab2 = st.tabs(["Explore Data", "CHW Triage Tool"])

    with tab1:
        render_explore_tab(filtered)

    with tab2:
        render_triage_tab(filtered)


if __name__ == "__main__":
    main()

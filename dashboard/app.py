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
DEFAULT_DATASET = REPO_ROOT / "synthetic-data" / "datasets" / "sample_with_conditions_200.csv"

AGE_BAND_ORDER = ["10-14", "15-19", "20-24", "25-34", "35-44", "45-54"]
FLOW_ORDER = ["light", "moderate", "heavy", "very_heavy"]

st.set_page_config(page_title="THRIVE Triage — Menstrual Health Decision Support", layout="wide")

LIGHT_BG = "#FAF9F6"
DARK_BG = "#0D1117"
DARK_CARD = "#161B22"
DARK_BORDER = "#30363D"

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
alt.themes.register("thrive-dark", lambda: {
    "config": {
        "view": {"stroke": DARK_BORDER},
        "background": DARK_BG,
        "title": {"color": "#F0F6FC"},
        "axis": {"labelFontSize": 12, "titleFontSize": 13, "grid": False,
                 "labelColor": "#8B949E", "titleColor": "#F0F6FC", "domainColor": DARK_BORDER, "tickColor": DARK_BORDER},
        "header": {"labelFontSize": 12, "titleFontSize": 13, "labelColor": "#F0F6FC", "titleColor": "#F0F6FC"},
        "legend": {"labelFontSize": 11, "labelColor": "#F0F6FC", "titleColor": "#F0F6FC"},
        "range": {
            "category": ["#58A6FF", "#FF7B72", "#3FB950", "#D29922", "#BC8CFF", "#79C0FF"],
            "diverging": ["#FF7B72", "#D29922", "#3FB950"],
            "heatmap": ["#0D1117", "#161B22", "#30363D"],
        },
    }
})
alt.themes.enable("thrive")

st.markdown("""
<style>
:root {
    --bg: #FAF9F6; --bg-card: #FFFFFF; --bg-card-alt: #F6F8FA;
    --text: #1A1A2E; --text-muted: #555; --text-caption: #888;
    --border: #ddd; --border-light: #E8E8E4;
    --focus: #006D77; --focus-ring: 0 0 0 3px rgba(0,109,119,0.3);
    --risk-high-bg: #FEF1F0; --risk-high-border: #D62828;
    --risk-mod-bg: #FFF8E7; --risk-mod-border: #FFB703;
    --risk-low-bg: #F0F9F6; --risk-low-border: #2A9D8F;
    --ref-bg: #FFF8E7; --ref-border: #FFB703;
    font-size: 16px;
}
.dark-mode {
    --bg: #0D1117; --bg-card: #161B22; --bg-card-alt: #0D1117;
    --text: #F0F6FC; --text-muted: #8B949E; --text-caption: #6E7681;
    --border: #30363D; --border-light: #21262D;
    --focus: #58A6FF; --focus-ring: 0 0 0 3px rgba(88,166,255,0.4);
    --risk-high-bg: #2D1517; --risk-high-border: #FF7B72;
    --risk-mod-bg: #2D2410; --risk-mod-border: #D29922;
    --risk-low-bg: #0F2D1B; --risk-low-border: #3FB950;
    --ref-bg: #2D2410; --ref-border: #D29922;
}
.stApp { background: var(--bg); color: var(--text); }
h1, h2, h3, .stTabs [data-baseweb="tab"], .stTabs [aria-selected="true"],
.stMarkdown, p, li, .stSelectbox label, .stMultiSelect label {
    color: var(--text) !important;
}
.stTabs [data-baseweb="tab"] { border-radius: 0.5rem 0.5rem 0 0; font-weight: 500; padding: 0.5rem 1rem; }
.stTabs [aria-selected="true"] { background: #006D77 !important; color: white !important; }
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
    background: var(--bg-card) !important; color: var(--text) !important; border-color: var(--border) !important;
}
.st-bb, .st-at, .st-ae, .st-af, .st-ag { background: var(--bg-card) !important; color: var(--text) !important; }
.stMetric, .stMetric label, .stMetric [data-testid="stMetricValue"] { color: var(--text) !important; }
.stMetric [data-testid="stMetricValue"] { font-weight: 700 !important; }
.dataframe { background: var(--bg-card) !important; color: var(--text) !important; }
.dataframe th { background: var(--bg-card-alt) !important; color: var(--text) !important; }
.dataframe td { border-color: var(--border) !important; color: var(--text) !important; }

*:focus-visible { outline: 2px solid var(--focus) !important; outline-offset: 2px; border-radius: 4px; }
.stSelectbox *:focus-visible, .stMultiSelect *:focus-visible,
.stTabs [data-baseweb="tab"]:focus-visible { box-shadow: var(--focus-ring); }

.stMarkdown p { line-height: 1.6; }
code { font-size: 0.85rem; }
.stCaption { color: var(--text-caption); }

.risk-high { background: var(--risk-high-bg); border-left: 4px solid var(--risk-high-border);
    padding: 0.75rem 1rem; border-radius: 0.5rem; margin: 0.5rem 0; color: var(--text); }
.risk-moderate { background: var(--risk-mod-bg); border-left: 4px solid var(--risk-mod-border);
    padding: 0.75rem 1rem; border-radius: 0.5rem; margin: 0.5rem 0; color: var(--text); }
.risk-low { background: var(--risk-low-bg); border-left: 4px solid var(--risk-low-border);
    padding: 0.75rem 1rem; border-radius: 0.5rem; margin: 0.5rem 0; color: var(--text); }
.risk-badge-high { background: var(--risk-high-border); color: white;
    padding: 0.1rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }
.risk-badge-moderate { background: var(--risk-mod-border); color: #1A1A2E;
    padding: 0.1rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }
.risk-badge-low { background: var(--risk-low-border); color: white;
    padding: 0.1rem 0.6rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }
.referral-box { background: var(--ref-bg); border: 1px solid var(--ref-border);
    border-radius: 0.5rem; padding: 0.75rem; margin-top: 0.5rem; color: var(--text); }
.patient-card { background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 0.75rem; padding: 1.25rem; color: var(--text); }
.stAlert { color: var(--text); border-color: var(--border); }
.stAlert > div { background: var(--bg-card) !important; }
@media (max-width: 768px) {
    .row-widget.stColumns { flex-direction: column; }
    .stTabs [data-baseweb="tab"] { font-size: 0.85rem; padding: 0.4rem 0.6rem; }
    h1 { font-size: 1.4rem; }
    h2 { font-size: 1.15rem; }
}
</style>
<script>
const m = window.matchMedia('(prefers-color-scheme: dark)');
function setTheme(e) {
    const d = document.documentElement;
    if (e.matches) { d.classList.add('dark-mode'); } else { d.classList.remove('dark-mode'); }
}
m.addEventListener('change', setTheme);
setTheme(m);
</script>
""", unsafe_allow_html=True)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["reported_symptoms"] = df["reported_symptoms"].fillna("")
    return df





def render_explore_tab(df: pd.DataFrame) -> None:
    cols = st.columns(4)
    cols[0].metric("Records", f"{len(df):,}")
    cols[1].metric("Median cycle", f"{df['cycle_length_days'].median():.0f} days")
    cols[2].metric("Median pain", f"{df['pain_score'].median():.0f} / 10")
    cols[3].metric("Missed school/work", f"{(df['missed_school_or_work'] == 'yes').mean():.0%}")

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
        f"<p style='color:var(--text-muted);margin-top:-0.5rem;' "
        f"lang='en' dir='auto'>"
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

        st.markdown("<div class='patient-card' dir='auto'>", unsafe_allow_html=True)
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
            st.markdown(f"<em dir='auto'>“{free_text}”</em>", unsafe_allow_html=True)
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
        cols = st.columns(3)
        for i, (cond, label) in enumerate([
            ("condition_iron_deficiency", "Iron Deficiency"),
            ("condition_fibroids", "Fibroids / Adenomyosis"),
            ("condition_coagulation_disorder", "Coagulation Disorder"),
        ]):
            actual = df[cond].eq("yes").astype(int)
            cond_key = "fibroids_adenomyosis" if cond == "condition_fibroids" else cond.replace("condition_", "")
            predicted = (risk_df[cond_key] >= 50).astype(int)
            correct = (actual == predicted).sum()
            cols[i].metric(f"{label} accuracy", f"{correct / len(df):.0%}")

        st.caption("Ground truth labels are synthetic — accuracy reflects the rule-based model against generated labels, not real clinical performance.")

def main() -> None:
    st.title("THRIVE Triage")
    st.markdown(
        f"<p style='color:var(--text-muted);margin-top:-0.75rem;margin-bottom:1.5rem;' "
        f"lang='en' dir='auto'>"
        "Menstrual health decision-support · "
        "<em>All data shown is synthetic — distributions are simulated.</em></p>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        dark = st.toggle("Dark mode", value=st.session_state.get("dark_mode", False),
                         key="dark_toggle", help="Switch between light and dark theme")
        if dark != st.session_state.get("dark_mode"):
            st.session_state.dark_mode = dark
            if dark:
                alt.themes.enable("thrive-dark")
            else:
                alt.themes.enable("thrive")
            st.rerun()

        st.markdown("---")
        uploaded = st.file_uploader("Load data (CSV)", type="csv")

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

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

PRIMARY = "#4A7C7A"
SECONDARY = "#D4897A"
CHART_COLORS = ["#4A7C7A", "#D4897A", "#7CA08A", "#C9A97A", "#9A7CA0", "#7A8CA0"]

DP_BG = "#1C1C24"
DP_CARD = "#262630"
DP_BORDER = "#363640"

alt.themes.register("thrive", lambda: {
    "config": {
        "view": {"stroke": "transparent"},
        "axis": {"labelFontSize": 12, "titleFontSize": 13, "grid": False, "labelColor": "#5A5A65",
                 "titleColor": "#3A3A45", "domainColor": "#E0E0E4", "tickColor": "#E0E0E4"},
        "header": {"labelFontSize": 12, "titleFontSize": 13},
        "legend": {"labelFontSize": 11},
        "range": {"category": CHART_COLORS, "diverging": ["#C4837A", "#C9A97A", "#7CA08A"],
                  "heatmap": ["#EDECE8", "#D4D0C8", "#4A7C7A"]},
    }
})
alt.themes.register("thrive-dark", lambda: {
    "config": {
        "view": {"stroke": DP_BORDER}, "background": DP_BG,
        "title": {"color": "#E4E4EC"},
        "axis": {"labelFontSize": 12, "titleFontSize": 13, "grid": False,
                 "labelColor": "#9A9AA8", "titleColor": "#E4E4EC", "domainColor": DP_BORDER, "tickColor": DP_BORDER},
        "header": {"labelFontSize": 12, "titleFontSize": 13, "labelColor": "#E4E4EC", "titleColor": "#E4E4EC"},
        "legend": {"labelFontSize": 11, "labelColor": "#E4E4EC", "titleColor": "#E4E4EC"},
        "range": {"category": ["#7CB8B6", "#E8A898", "#9ABAA4", "#D4BA8A", "#B49AB8", "#9AAAB8"],
                  "diverging": ["#D4897A", "#C9A97A", "#7CA08A"],
                  "heatmap": ["#1C1C24", "#262630", "#363640"]},
    }
})
alt.themes.enable("thrive")

st.markdown("""
<style>
:root {
    --bg: #F5F4F0; --bg-card: #FFFFFF; --bg-card-alt: #F0EFEA;
    --text: #2D2D35; --text-muted: #6A6A75; --text-caption: #9A9AA5;
    --shadow: 0 1px 4px rgba(0,0,0,0.06);
    --focus: #4A7C7A; --focus-ring: 0 0 0 3px rgba(74,124,122,0.25);
    --hr: #E0DED8;
    --risk-high-bg: #F7ECEB; --risk-high-border: #C4837A;
    --risk-mod-bg: #F6EEE1; --risk-mod-border: #C9A97A;
    --risk-low-bg: #E8EFE9; --risk-low-border: #7CA08A;
    --ref-bg: #F6EEE1; --ref-border: #C9A97A;
    font-size: 16px;
}
.dark-mode {
    --bg: #1C1C24; --bg-card: #262630; --bg-card-alt: #1C1C24;
    --text: #E4E4EC; --text-muted: #9A9AA8; --text-caption: #7A7A88;
    --shadow: 0 1px 4px rgba(0,0,0,0.3);
    --focus: #7CB8B6; --focus-ring: 0 0 0 3px rgba(124,184,182,0.3);
    --hr: #363640;
    --risk-high-bg: #2D1E1D; --risk-high-border: #C4837A;
    --risk-mod-bg: #2D2619; --risk-mod-border: #C9A97A;
    --risk-low-bg: #1A2B1E; --risk-low-border: #7CA08A;
    --ref-bg: #2D2619; --ref-border: #C9A97A;
}
.stApp { background: var(--bg); color: var(--text); }
h1 { font-size: 1.65rem; font-weight: 700; letter-spacing: -0.02em; color: var(--text) !important; }
h2 { font-size: 1.2rem; font-weight: 600; color: var(--text) !important; }
h3 { font-size: 1rem; font-weight: 600; color: var(--text) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: var(--bg-card); padding: 4px; border-radius: 10px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; font-weight: 500; font-size: 0.9rem;
    padding: 0.4rem 1rem; color: var(--text-muted) !important; border: none !important; }
.stTabs [aria-selected="true"] { background: var(--bg) !important; color: var(--text) !important;
    box-shadow: var(--shadow); }
.stSelectbox label, .stMultiSelect label { color: var(--text) !important; font-weight: 500; font-size: 0.85rem; }
.stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
    background: var(--bg-card) !important; color: var(--text) !important;
    border: 1px solid var(--hr) !important; border-radius: 8px !important; box-shadow: var(--shadow); }
.st-bb, .st-at, .st-ae, .st-af, .st-ag, .st-cd, .st-ce { background: var(--bg-card) !important; color: var(--text) !important; }
.stSelectbox li[role="option"], .stMultiSelect li[role="option"] { color: var(--text) !important; }
.stSelectbox li[role="option"]:hover, .stMultiSelect li[role="option"]:hover { background: var(--bg-card-alt) !important; }
div[data-baseweb="menu"] { background: var(--bg-card) !important; border: 1px solid var(--hr) !important; border-radius: 8px !important; }
.stSelectbox input::placeholder, .stMultiSelect input::placeholder { color: var(--text-caption) !important; opacity: 0.7; }
.stSelectbox [data-testid="stSelectbox"] [data-baseweb="select"] span, .stMultiSelect span {
    color: var(--text) !important; }
.stButton > button { background: var(--bg-card) !important; color: var(--text) !important;
    border: 1px solid var(--hr) !important; border-radius: 8px !important; }
.stMetric { background: var(--bg-card); padding: 0.75rem 1rem; border-radius: 10px;
    box-shadow: var(--shadow); }
.stMetric label { color: var(--text-muted) !important; font-weight: 500 !important; font-size: 0.8rem; }
.stMetric [data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 700 !important; font-size: 1.5rem; }
.dataframe { background: var(--bg-card) !important; color: var(--text) !important;
    border-radius: 10px; }
.dataframe th { background: var(--bg-card-alt) !important; color: var(--text) !important; }
.dataframe td { border-color: var(--hr) !important; color: var(--text) !important; }
.stAlert { background: var(--bg-card) !important; color: var(--text); border: 1px solid var(--hr); border-radius: 8px; }
hr { border-color: var(--hr) !important; }
.stMarkdown p { line-height: 1.6; }
.stCaption { color: var(--text-caption); }

*:focus-visible { outline: 2px solid var(--focus) !important; outline-offset: 2px; border-radius: 4px; }
.stSelectbox *:focus-visible, .stMultiSelect *:focus-visible,
.stTabs [data-baseweb="tab"]:focus-visible { box-shadow: var(--focus-ring); }

.risk-high { background: var(--risk-high-bg); border-left: 4px solid var(--risk-high-border);
    padding: 0.75rem 1rem; border-radius: 8px; margin: 0.5rem 0; color: var(--text);
    box-shadow: var(--shadow); }
.risk-moderate { background: var(--risk-mod-bg); border-left: 4px solid var(--risk-mod-border);
    padding: 0.75rem 1rem; border-radius: 8px; margin: 0.5rem 0; color: var(--text);
    box-shadow: var(--shadow); }
.risk-low { background: var(--risk-low-bg); border-left: 4px solid var(--risk-low-border);
    padding: 0.75rem 1rem; border-radius: 8px; margin: 0.5rem 0; color: var(--text);
    box-shadow: var(--shadow); }
.risk-badge-high { background: var(--risk-high-border); color: white;
    padding: 0.1rem 0.6rem; border-radius: 1rem; font-size: 0.7rem; font-weight: 700; }
.risk-badge-moderate { background: var(--risk-mod-border); color: #2D2D35;
    padding: 0.1rem 0.6rem; border-radius: 1rem; font-size: 0.7rem; font-weight: 700; }
.risk-badge-low { background: var(--risk-low-border); color: white;
    padding: 0.1rem 0.6rem; border-radius: 1rem; font-size: 0.7rem; font-weight: 700; }
.referral-box { background: var(--ref-bg); border: 1px solid var(--ref-border);
    border-radius: 8px; padding: 0.75rem; margin-top: 0.5rem; color: var(--text); }
.patient-card { background: var(--bg-card); border-radius: 10px; padding: 1.25rem;
    color: var(--text); box-shadow: var(--shadow); }
.stSidebar .stApp { background: var(--bg-card-alt); }
.stSidebar section { background: var(--bg-card-alt); }
.stSidebar [data-testid="stSidebarContent"] { background: var(--bg-card-alt); padding: 1.5rem 1rem; }
.stSidebar h2, .stSidebar h3 { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;
    color: var(--text-muted) !important; margin-top: 1rem; }
.stSidebar .stFileUploader section { background: var(--bg-card); border: 2px dashed var(--hr) !important;
    border-radius: 10px; padding: 0.75rem; }
.stSidebar .stFileUploader section:hover { border-color: var(--focus) !important;
    background: var(--bg-card-alt) !important; }
.stSidebar .stFileUploader [data-testid="stFileUploaderDropzone"] { min-height: 4rem; }
.stSidebar .stFileUploader button { background: var(--bg-card) !important; color: var(--text) !important;
    border: 1px solid var(--hr) !important; border-radius: 8px !important; font-size: 0.85rem; }
.stSidebar .stFileUploader button:hover { border-color: var(--focus) !important; }
.stSidebar .stMultiSelect div[data-baseweb="select"] > div {
    background: var(--bg-card) !important; border-radius: 8px !important; min-height: 2.4rem; }
.stSidebar .stMultiSelect div[data-baseweb="select"] > div:hover { border-color: var(--focus) !important; }
.stSidebar .stSelectbox div[data-baseweb="select"] > div {
    background: var(--bg-card) !important; border-radius: 8px !important; min-height: 2.4rem; }
.stSidebar .stSelectbox div[data-baseweb="select"] > div:hover { border-color: var(--focus) !important; }
.stSidebar .stToggle { padding: 0.5rem 0; }
.stSidebar .stToggle label { font-size: 0.85rem; font-weight: 500; color: var(--text) !important; }
@media (max-width: 768px) {
    .row-widget.stColumns { flex-direction: column; }
    h1 { font-size: 1.3rem; }
    h2 { font-size: 1rem; }
    .stMetric [data-testid="stMetricValue"] { font-size: 1.2rem; }
}
</style>
<script>
const m = window.matchMedia('(prefers-color-scheme: dark)');
function setTheme(e) { document.documentElement.classList.toggle('dark-mode', e.matches); }
m.addEventListener('change', setTheme); setTheme(m);
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
                                scale=alt.Scale(range=["#C4D4C2", "#7CA08A", "#D4897A", "#C4837A"])),
            ).properties(height=250),
            use_container_width=True,
        )

        st.subheader("Cycle length distribution")
        st.altair_chart(
            alt.Chart(df).mark_bar(color="#4A7C7A", opacity=0.8).encode(
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
            alt.Chart(symptom_counts).mark_bar(color="#D4897A", opacity=0.8).encode(
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
                                scale=alt.Scale(range=["#4A7C7A", "#7CA08A", "#D4897A", "#9A7CA0"])),
            ).properties(height=200),
            use_container_width=True,
        )

    st.subheader("Records over time")
    st.altair_chart(
        alt.Chart(df).mark_line(point=True, color="#4A7C7A", strokeWidth=2).encode(
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
                                            range=["#4A7C7A", "#D4897A", "#7CA08A"])),
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
        st.markdown(f"<div style='font-size:0.8rem;font-weight:600;color:var(--text-muted);"
                    f"text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1rem;'>"
                    f"THRIVE Triage · v0.2</div>", unsafe_allow_html=True)

        uploaded = st.file_uploader("Upload data", type="csv",
                                    help="Upload a CSV file with menstrual health records")

        dark = st.toggle("Dark mode", value=st.session_state.get("dark_mode", False),
                         key="dark_toggle", help="Switch between light and dark theme")
        if dark != st.session_state.get("dark_mode"):
            st.session_state.dark_mode = dark
            if dark:
                alt.themes.enable("thrive-dark")
            else:
                alt.themes.enable("thrive")
            st.rerun()

    if uploaded is not None:
        df = pd.read_csv(uploaded)
        df["reported_symptoms"] = df["reported_symptoms"].fillna("")
    else:
        df = load_data(DEFAULT_DATASET)

    st.sidebar.markdown("Filters")
    st.sidebar.markdown(f"<hr style='margin:0.25rem 0 0.75rem 0;border-color:var(--hr);'>",
                        unsafe_allow_html=True)
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

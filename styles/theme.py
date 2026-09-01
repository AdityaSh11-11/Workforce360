import streamlit as st
from datetime import datetime

# ==========================================================
# ENTERPRISE DARK THEME - INSIGHTFORGE AI V2
# ==========================================================

PRIMARY = "#2563EB"
SUCCESS = "#16A34A"
WARNING = "#F59E0B"
DANGER = "#DC2626"

BACKGROUND = "#0B1120"
SURFACE = "#111827"
CARD = "#172033"
BORDER = "#243042"

TEXT = "#F8FAFC"
SUBTEXT = "#CBD5E1"


# ==========================================================
# LOAD GLOBAL THEME
# ==========================================================

def load_theme():

    st.markdown(f"""
<style>

/* ---------- Background ---------- */

.stApp {{
    background-color: {BACKGROUND};
}}

.main .block-container {{
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}}

/* ---------- Sidebar ---------- */

[data-testid="stSidebar"] {{
    background-color: {SURFACE};
    border-right:1px solid {BORDER};
}}

[data-testid="stSidebar"] * {{
    color:{TEXT};
}}

/* ---------- Typography ---------- */

html, body, [class*="css"] {{
    font-family: "Segoe UI", sans-serif;
}}

h1,h2,h3,h4,h5,h6 {{
    color:{TEXT};
}}

p {{
    color:{SUBTEXT};
    line-height:1.7;
}}

small {{
    color:#94A3B8;
}}

/* ---------- Buttons ---------- */

.stButton>button {{
    background:{PRIMARY};
    color:white;
    border:none;
    border-radius:12px;
    height:46px;
    width:100%;
    font-weight:600;
}}

.stButton>button:hover {{
    background:#1D4ED8;
    color:white;
}}

/* ---------- Inputs ---------- */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {{
    background:{CARD};
    color:white;
    border-radius:10px;
    border:1px solid {BORDER};
}}

.stFileUploader {{
    border:2px dashed {PRIMARY};
    border-radius:12px;
    background:{CARD};
    padding:12px;
}}

.stSlider {{
    color:{PRIMARY};
}}

/* ---------- Dataframe ---------- */

[data-testid="stDataFrame"] {{
    border:1px solid {BORDER};
    border-radius:14px;
    overflow:hidden;
}}

table {{
    color:white;
}}

/* ---------- Metric ---------- */

[data-testid="metric-container"] {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:16px;
    padding:16px;
}}

[data-testid="metric-container"] label {{
    color:#94A3B8;
}}

[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color:white;
}}

/* ---------- Expander ---------- */

.streamlit-expanderHeader {{
    color:white;
    font-weight:600;
}}

details {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:12px;
    padding:8px;
}}

/* ---------- Tabs ---------- */

button[data-baseweb="tab"] {{
    color:#CBD5E1;
    font-weight:600;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color:white;
    border-bottom:2px solid {PRIMARY};
}}

/* ---------- Divider ---------- */

hr {{
    border-color:{BORDER};
}}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HERO
# ==========================================================

def hero(title, subtitle):
    with st.container(border=True):
        st.markdown(f"# {title}")
        st.caption(subtitle)


# ==========================================================
# PAGE TITLE
# ==========================================================

def page_title(title, description=""):

    st.markdown(f"## {title}")

    if description:
        st.caption(description)

    st.divider()


# ==========================================================
# SECTION TITLE
# ==========================================================

def section(title, description=""):

    st.markdown(
        f"""
### {title}
""")

    if description:
        st.caption(description)


# ==========================================================
# SUBSECTION TITLE
# ==========================================================

def subsection(title, description=""):

    st.markdown(f"#### {title}")

    if description:
        st.caption(description)


# ==========================================================
# FOOTER
# ==========================================================

def footer():

    st.divider()

    year = datetime.now().year

    st.markdown(
        f"""
<div style="
text-align:center;
font-size:13px;
color:#64748B;
padding:10px;
">
InsightForge AI Workforce Intelligence Platform • Version 2.0 • {year}
</div>
""",
        unsafe_allow_html=True
    )
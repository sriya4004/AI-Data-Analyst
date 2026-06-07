import sys
from pathlib import Path

_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

from utils.api_client import health
from utils.config import get_api_base
from utils.theme import apply_theme

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon=":material/dashboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

ok, body = health()

st.markdown('<div class="health-card"><span class="label">Enterprise analytics experience</span><div class="status">AI Data Analyst is ready to guide your team from raw data to trusted business decisions.</div><div class="badge">Premium analytics experience</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1])
with col1:
    st.markdown('<h1 class="hero-title">AI Data Analyst</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">A polished analytics workspace for modern businesses. Upload data, validate workflows, generate actionable insights, forecast outcomes, and interact with a powerful AI agent in one professional platform.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-subtitle">Designed for teams that need fast business intelligence without sacrificing clarity, trust, or presentation quality.</div>',
        unsafe_allow_html=True,
    )
with col2:
    if ok:
        status = 'Connected'
        status_message = f'API reachable — {get_api_base()}'
    else:
        status = 'Disconnected'
        status_message = f'Could not reach API at {get_api_base()}. Start the backend: uvicorn backend.main:app --reload or set API_BASE_URL.'
    health_html = (
        '<div class="health-card">'
        '<span class="label">Backend status</span>'
        f'<div class="status">{status}</div>'
        f'<div>{status_message}</div>'
        '</div>'
    )
    st.markdown(health_html, unsafe_allow_html=True)
    if not ok and isinstance(body, dict) and body.get('error'):
        st.caption(body['error'])

st.divider()
st.markdown('### Built for confident analytics and rapid decision-making')
feature_cols = st.columns(4)
features = [
    ('📤 Dataset onboarding', 'Capture and validate CSV/XLSX data with a modern intake workflow.'),
    ('💡 Insight suite', 'Generate summaries, KPI dashboards, forecasts, and narrative intelligence.'),
    ('📊 Workflow intelligence', 'Review pipeline transformations, dependency chains, and SQL flow.'),
    ('🤖 AI analyst', 'Collaborate with the agent to answer questions, create charts, and refine decisions.'),
]
for index, (title, description) in enumerate(features, start=1):
    style_class = f'accent-{index}'
    feature_cols[index - 1].markdown(
        f'<div class="feature-card {style_class}"><h4>{title}</h4><p>{description}</p></div>',
        unsafe_allow_html=True,
    )

st.divider()
st.markdown("**Quick navigation**")
st.markdown("- **Dataset Onboarding** — register CSV/XLSX and review cleaning summary, schema, and preview")
st.markdown("- **Registered Datasets** — view registered dataset names and metadata")
st.markdown("- **Insights Suite** — produce business insights and visual summaries")
st.markdown("- **Workflow Intelligence** — inspect the SQL pipeline and end-to-end data flow")
st.markdown("- **AI Analyst** — interact with the AI agent and visualize chart recommendations")

import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

st.set_page_config(
    page_title="Workflow Intelligence",
    page_icon=":material/data_usage:",
    layout="wide",
)

from utils.api_client import list_datasets, workflow_analysis
from utils.config import get_api_base
from utils.present import display_workflow_response
from utils.theme import apply_theme

apply_theme()

st.title("Workflow intelligence")
st.caption(f"POST /workflow-analysis (LangGraph) — `{get_api_base()}`")

ok, data = list_datasets()
names = (data or {}).get("datasets") if ok else []
if not names:
    st.warning("No datasets registered. Upload a file first.")
    st.stop()

ds = st.selectbox("Dataset", names, index=0)
question = st.text_area(
    "Question",
    placeholder="e.g. What is the average revenue by region?",
    height=120,
)
if st.button("Run workflow", type="primary") and question.strip():
    with st.spinner("Running analyst graph…"):
        ok2, resp = workflow_analysis(ds, question.strip())
    if ok2:
        display_workflow_response(resp)
    else:
        st.error("Workflow failed")
        st.json(resp)

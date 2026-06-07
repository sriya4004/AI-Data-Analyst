import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

st.set_page_config(
    page_title="Insights Suite",
    page_icon=":material/lightbulb:",
    layout="wide",
)

from utils.api_client import generate_insights, list_datasets
from utils.config import get_api_base
from utils.present import display_insights_response
from utils.theme import apply_theme

apply_theme()

st.title("Insights suite")
st.caption(f"GET /generate-insights — `{get_api_base()}`")

ok, data = list_datasets()
names = (data or {}).get("datasets") if ok else []
if not names:
    st.warning("No datasets registered. Upload a file first.")
    st.stop()

choice = st.selectbox("Dataset", names, index=0)
if st.button("Run", type="primary"):
    with st.spinner("Calling API…"):
        ok2, resp = generate_insights(choice)
    if ok2:
        display_insights_response(resp)
    else:
        st.error("Request failed")
        st.json(resp)

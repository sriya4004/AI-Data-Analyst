import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

st.set_page_config(
    page_title="AI Analyst",
    page_icon=":material/smart_toy:",
    layout="wide",
)

from utils.api_client import list_datasets, run_agent
from utils.config import get_api_base
from utils.present import display_agent_response
from utils.theme import apply_theme

apply_theme()

st.title("AI analyst")
st.caption(
    f"POST /agent — routes to SQL, insights, or forecasting — `{get_api_base()}`"
)

ok, data = list_datasets()
names = (data or {}).get("datasets") if ok else []
if not names:
    st.warning("No datasets registered. Upload a file first.")
    st.stop()

ds = st.selectbox("Dataset", names, index=0)
question = st.text_area(
    "Your question",
    placeholder="e.g. Show a bar chart of total sales by category, or forecast revenue for the next month",
    height=140,
)

with st.expander("Forecasting options (optional)", expanded=False):
    st.markdown(
        "If you ask for predictions, you can pin **date** and **target** columns; "
        "otherwise the backend may auto-detect."
    )
    c1, c2 = st.columns(2)
    date_col = c1.text_input("Date column", placeholder="order_date")
    target_col = c2.text_input("Target column", placeholder="revenue")

if st.button("Ask agent", type="primary") and question.strip():
    with st.spinner("Agent running…"):
        ok2, resp = run_agent(
            ds,
            question.strip(),
            date_column=date_col.strip() or None,
            target_column=target_col.strip() or None,
        )
    if ok2:
        display_agent_response(resp)
    else:
        st.error("Agent request failed")
        st.json(resp)

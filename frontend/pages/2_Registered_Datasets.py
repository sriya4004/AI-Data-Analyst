import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

st.set_page_config(
    page_title="Registered Datasets",
    page_icon=":material/folder:",
    layout="wide",
)

import pandas as pd

from utils.api_client import list_datasets
from utils.config import get_api_base
from utils.theme import apply_theme

apply_theme()

st.title("Registered datasets")
st.caption(f"GET /datasets — `{get_api_base()}`")

if st.button("Refresh"):
    st.session_state.pop("datasets_cache", None)

ok, data = list_datasets()
if not ok:
    st.error("Failed to load datasets")
    st.json(data)
else:
    names = (data or {}).get("datasets") or []
    if not names:
        st.info("No datasets yet. Upload one on **Dataset Onboarding**.")
    else:
        st.dataframe(
            pd.DataFrame({"dataset_name": names}),
            use_container_width=True,
            hide_index=True,
        )

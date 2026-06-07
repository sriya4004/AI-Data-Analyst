import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import streamlit as st

st.set_page_config(
    page_title="Dataset Onboarding",
    page_icon=":material/cloud_upload:",
    layout="wide",
)

from utils.api_client import upload_file
from utils.config import get_api_base
from utils.present import display_upload_response
from utils.theme import apply_theme

apply_theme()

st.title("Dataset onboarding")
st.caption(f"API: `{get_api_base()}`")

uploaded = st.file_uploader(
    "CSV or XLSX",
    type=["csv", "xlsx"],
    help="Files are sent to POST /upload and registered for analysis.",
)

if uploaded is not None and st.button("Upload & register", type="primary"):
    data = uploaded.getvalue()
    ok, resp = upload_file(data, uploaded.name)
    if ok:
        st.session_state["last_upload"] = resp
        st.session_state["datasets"] = resp.get("registered_datasets") or []
        st.rerun()
    else:
        st.session_state.pop("last_upload", None)
        st.error("Upload failed")
        st.json(resp)

if st.session_state.get("last_upload"):
    st.divider()
    st.subheader("Latest registered upload")
    display_upload_response(st.session_state["last_upload"])

from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from utils.charts import render_forecast_chart, render_query_chart


def display_upload_response(data: Dict[str, Any]) -> None:
    st.success(data.get("message", "Upload complete"))
    c1, c2, c3, c4 = st.columns(4)
    info = data.get("dataset_info") or {}
    report = data.get("cleaning_report") or {}
    with c1:
        st.metric("Rows", info.get("rows", "—"))
    with c2:
        st.metric("Columns", info.get("columns", "—"))
    with c3:
        st.metric("Duplicates removed", report.get("duplicates_removed", "—"))
    with c4:
        st.metric("Missing values filled", report.get("missing_values_filled", "—"))

    st.subheader("Schema")
    schema = data.get("schema") or {}
    if schema:
        st.dataframe(
            pd.DataFrame(
                [{"column": k, "dtype": v} for k, v in schema.items()],
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("Preview")
    preview = data.get("preview") or []
    if preview:
        st.dataframe(pd.DataFrame(preview), use_container_width=True, hide_index=True)

    st.subheader("Registered datasets")
    names: List[str] = data.get("registered_datasets") or []
    if names:
        st.caption("Use these exact names in other pages.")
        st.code("\n".join(names), language=None)
    else:
        st.info("No datasets registered yet.")


def display_insights_response(data: Dict[str, Any]) -> None:
    if data.get("error"):
        st.error(data["error"])
        return
    st.subheader("Dataset")
    st.write(data.get("dataset", ""))
    info = data.get("dataset_info") or {}
    if info:
        m1, m2 = st.columns(2)
        m1.metric("Rows", info.get("rows", "—"))
        m2.metric("Columns", info.get("columns", "—"))
        cols = info.get("column_names") or []
        if cols:
            with st.expander("Column names"):
                st.write(", ".join(str(c) for c in cols))
    st.subheader("Insights")
    st.markdown(data.get("insights") or "_No content_")


def display_workflow_response(data: Dict[str, Any]) -> None:
    st.subheader("Generated SQL")
    st.code(data.get("generated_sql") or "", language="sql")
    st.subheader("Query result")
    qr = data.get("query_result") or []
    if qr:
        st.dataframe(pd.DataFrame(qr), use_container_width=True, hide_index=True)
    else:
        st.info("No rows returned.")
    st.subheader("Analysis")
    st.markdown(data.get("analysis") or "_No analysis_")


def display_sql_agent_result(result: Dict[str, Any]) -> None:
    st.markdown("#### SQL workflow")
    with st.expander("Schema (columns & dtypes)", expanded=False):
        st.json(result.get("schema") or {})
    display_workflow_response(result)
    chart_cfg = result.get("chart_config") or {}
    qr = result.get("query_result") or []
    fig = render_query_chart(chart_cfg, qr)
    if fig is not None:
        st.markdown("#### Chart")
        st.plotly_chart(fig, use_container_width=True)
    elif chart_cfg:
        st.caption(f"Chart suggestion: **{chart_cfg.get('chart_type', 'bar')}** — could not plot automatically.")


def display_forecast_result(result: Dict[str, Any]) -> None:
    if result.get("status") != "success":
        st.error(result.get("message", "Forecast failed"))
        return
    c1, c2 = st.columns(2)
    c1.metric("Target", str(result.get("target_column", "—")))
    c2.metric("Date column", str(result.get("date_column", "—")))
    det_d = result.get("detected_date_column")
    det_t = result.get("detected_target_column")
    if det_d or det_t:
        parts = []
        if det_d:
            parts.append(f"Date auto-detected: **{det_d}**")
        if det_t:
            parts.append(f"Target auto-detected: **{det_t}**")
        st.caption(" · ".join(parts))
    if result.get("insight"):
        st.info(result["insight"])
    fc = result.get("forecast") or []
    if fc:
        with st.expander("Forecast table (scroll)", expanded=False):
            st.dataframe(pd.DataFrame(fc), use_container_width=True, hide_index=True)
    fig = render_forecast_chart(result.get("chart_config") or {})
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)


def display_agent_response(payload: Dict[str, Any]) -> None:
    task = payload.get("task_type", "unknown")
    st.markdown(f"**Task type:** `{task}`")
    result = payload.get("result") or {}

    if isinstance(result, dict) and result.get("status") == "error":
        st.error(result.get("message", result.get("detail", "Error")))
        return

    if "sql_analysis" in str(task):
        display_sql_agent_result(result)
        return

    if "forecasting" in str(task):
        display_forecast_result(result)
        return

    if "insight_generation" in str(task):
        display_insights_response(result)
        return

    st.json(result)

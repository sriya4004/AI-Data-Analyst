from __future__ import annotations

from typing import Any, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _df_from_records(rows: List[dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def _pick_numeric_column(df: pd.DataFrame, preferred: Optional[str]) -> Optional[str]:
    if preferred and preferred in df.columns and pd.api.types.is_numeric_dtype(df[preferred]):
        return preferred
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            return str(col)
    return None


def _pick_category_column(df: pd.DataFrame, preferred: Optional[str]) -> Optional[str]:
    if preferred and preferred in df.columns:
        return preferred
    for col in df.columns:
        if col != preferred and not pd.api.types.is_numeric_dtype(df[col]):
            return str(col)
    if len(df.columns) > 0:
        return str(df.columns[0])
    return None


def render_query_chart(chart_config: dict, query_result: List[dict]) -> Optional[go.Figure]:
    """
    Build a Plotly figure from visualization_agent chart_config + SQL query_result.
    """
    df = _df_from_records(query_result)
    if df.empty:
        return None

    ctype = (chart_config or {}).get("chart_type", "bar") or "bar"
    x_col = (chart_config or {}).get("x_column") or None
    y_col = (chart_config or {}).get("y_column") or None

    x = _pick_category_column(df, x_col if x_col in df.columns else None)
    y = _pick_numeric_column(df, y_col if y_col in df.columns else None)

    if not x and len(df.columns) >= 1:
        x = str(df.columns[0])
    if not y and len(df.columns) >= 2:
        y = _pick_numeric_column(df, None)
    if not y:
        return None

    title = f"{ctype.title()} chart"
    try:
        if ctype == "line":
            fig = px.line(df, x=x, y=y, markers=True, title=title)
        elif ctype == "pie":
            fig = px.pie(df, names=x, values=y, title=title)
        elif ctype == "scatter":
            fig = px.scatter(df, x=x, y=y, title=title)
        else:
            fig = px.bar(df, x=x, y=y, title=title)
        fig.update_layout(template="plotly_white", margin=dict(l=40, r=20, t=50, b=40))
        return fig
    except Exception:
        fig = px.bar(df, x=x, y=y, title=title)
        fig.update_layout(template="plotly_white", margin=dict(l=40, r=20, t=50, b=40))
        return fig


def render_forecast_chart(chart_config: dict) -> Optional[go.Figure]:
    """
    Build a Plotly figure from forecast_chart_service JSON.
    """
    if not chart_config:
        return None

    combined = chart_config.get("combinedData") or []
    if not combined:
        return None

    df = pd.DataFrame(combined)
    if df.empty or "date" not in df.columns:
        return None

    title = chart_config.get("title") or "Forecast"
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["upper"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["lower"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(99, 102, 241, 0.2)",
            name="95% interval",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["predicted"],
            mode="lines",
            name="Predicted",
            line=dict(color="#6366f1", width=3),
        )
    )
    fig.update_layout(
        title=title,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis_title="Date",
        yaxis_title=chart_config.get("yAxis", {}).get("label", "Value"),
    )
    return fig

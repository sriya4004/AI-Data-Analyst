# AI Data Analyst Agent

An AI-powered Business Intelligence and Analytics Platform built using FastAPI, LangGraph, OpenRouter LLMs, DuckDB, Prophet, and Multi-Agent AI Workflows.

The platform allows users to upload CSV/Excel datasets, ask analytical questions in natural language, generate charts dynamically, obtain AI-driven business insights, and perform autonomous data analysis and time-series forecasting using specialized AI agents.

---

# Features

## Dataset Management
- Upload CSV and Excel datasets
- Automatic dataset registration
- Dataset preview and schema extraction
- Dataset cleaning and preprocessing

---

## AI-Powered Analytics
- Natural language analytical queries
- AI-generated SQL queries
- DuckDB-powered analytical execution
- Business insight generation
- KPI extraction and grounded analytics

---

## AI Forecasting & Predictive Analytics
- **Time-Series Forecasting**: Automated forecasting using Facebook Prophet.
- **Trend Detection**: AI-driven analysis of upward, downward, and stable trends.
- **Predictive Insights**: Natural-language business insights derived from forecast models.
- **Confidence Intervals**: Visual representation of prediction uncertainty (95% CI).
- **Automated Chart Config**: Frontend-ready JSON configurations for forecast visualizations.

---

## Dynamic Visualization
- AI-generated chart configurations
- Automatic chart type selection
- Frontend-ready visualization JSON

Supported chart types:
- Bar charts
- Line charts
- Pie charts
- Scatter plots
- **Forecast charts** (with confidence intervals)

---

## Multi-Agent Architecture
- **Supervisor Agent**: Intelligently routes user requests based on intent classification.
- **SQL Analysis Agent**: Generates and executes analytical SQL queries.
- **Forecast Agent**: Orchestrates time-series predictions and trend analysis.
- **Insight Generation Agent**: Produces descriptive business insights from data.
- **Visualization Agent**: Determines the best visual representation for results.

---

# Tech Stack

## Backend
- FastAPI
- Python
- DuckDB
- Pandas
- **Prophet** (Time-Series Forecasting)
- LangChain / LangGraph
- OpenRouter API

---

## AI & Analytics
- OpenRouter LLMs (GPT-4o / Claude 3.5 Sonnet)
- Multi-Agent AI Architecture
- Workflow Orchestration
- KPI Grounding
- AI-driven SQL & Insight Generation

---

# AI Forecasting & Predictive Analytics

The platform features a specialized forecasting subsystem designed to provide stakeholders with future-looking metrics.

### Forecasting Architecture
The forecasting system operates as a specialized agent-led workflow:
1. **Intent Classification**: The Supervisor Agent detects forecasting intent (keywords: *forecast, predict, future, projection*).
2. **Validation**: The system ensures the dataset contains valid date and numeric columns.
3. **Modeling**: The Forecast Service utilizes **Facebook Prophet** for robust time-series modeling, handling seasonality and outliers automatically.
4. **Insight Generation**: The Forecast Insight Service analyzes the model's slope and generates a natural-language business narrative.
5. **Visualization**: The Forecast Chart Service produces a JSON configuration including predictions and confidence intervals for frontend rendering.

### Capabilities
- **Revenue & Sales Prediction**: Predict future financial performance based on historical data.
- **Confidence Interval Analysis**: Understand the upper and lower bounds of predictions.
- **Automated Trend Detection**: Immediate identification of growth, decline, or stability.

### API Request Example
```http
POST /agent
Content-Type: application/json

{
    "dataset_name": "sales_data.csv",
    "question": "Predict our revenue for the next 30 days",
    "date_column": "order_date",
    "target_column": "revenue"
}
```

### API Response Example
```json
{
    "task_type": "forecasting",
    "result": {
        "status": "success",
        "agent": "Forecast Agent",
        "dataset": "sales_data.csv",
        "target_column": "revenue",
        "insight": "Revenue is expected to increase over the next 30 days based on a strong upward trend.",
        "forecast": [...],
        "chart_config": {
            "type": "forecast_chart",
            "datasets": [
                { "label": "Predicted Value", "data": [105.2, 108.4, ...] },
                { "label": "Confidence Interval", "data": [{"low": 98.1, "high": 112.3}, ...] }
            ]
        }
    }
}
```

---

# Project Architecture

```text
User
 ↓
Frontend Dashboard
 ↓
FastAPI APIs
 ↓
Supervisor Agent
 ↓
Specialized Agents (SQL, Forecast, Insight, Viz)
 ↓
LangGraph Workflows
 ↓
Services (Prophet, DuckDB, LLM)
 ↓
Datasets
```

---

# Folder Structure

```text
backend/
├── agents/
│   ├── supervisor_agent.py
│   ├── sql_agent.py
│   ├── forecast_agent.py          # NEW: Orchestrates forecasting tasks
│   ├── insight_agent.py
│   └── visualization_agent.py
│
├── api/
│   └── agent.py                   # Main entry point for AI agents
│
├── services/
│   ├── forecast_service.py        # NEW: Prophet model execution
│   ├── forecast_validator.py      # NEW: Input validation for forecasting
│   ├── forecast_insight_service.py # NEW: Trend & NL insight generation
│   ├── forecast_chart_service.py   # NEW: Frontend-ready chart configs
│   ├── llm_service.py
│   ├── visualization_service.py
│   └── insight_service.py
│
├── main.py
```

---

# Installation & Setup

1. **Clone & Install**:
   ```bash
   git clone <repo-url>
   pip install -r requirements.txt
   ```
2. **Environment**:
   Set `OPENROUTER_API_KEY` in your `.env` file.
3. **Run**:
   ```bash
   uvicorn backend.main:app --reload
   ```

---

# Current Completed Features
* Dataset Upload & Registry
* Multi-Agent Intent Routing
* AI-Generated SQL Analytics (DuckDB)
* **AI Forecasting & Predictive Analytics (Prophet)**
* **Natural-Language Forecast Insights**
* **Dynamic Forecast Chart Configurations**
* LangGraph Workflow Orchestration
* Business Insight Generation

---

# Team Responsibilities

### Atia Naim
* AI Backend Architecture & Multi-Agent System
* LangGraph Workflow Orchestration

### Sriya Pandey
* **Forecasting & Predictive Analytics**
* Prophet Integration & Statistical Intelligence
* Trend Analysis & Insight Logic

### Amaan Shahid
* Frontend Dashboard & UI/UX Development
* API Integration & Deployment

---

# License
MIT License

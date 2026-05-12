````md
# AI Data Analyst Agent

An AI-powered Business Intelligence and Analytics Platform built using FastAPI, LangGraph, OpenRouter LLMs, DuckDB, and Multi-Agent AI Workflows.

The platform allows users to upload CSV/Excel datasets, ask analytical questions in natural language, generate charts dynamically, obtain AI-driven business insights, and perform autonomous data analysis using specialized AI agents.

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

## Dynamic Visualization
- AI-generated chart configurations
- Automatic chart type selection
- Frontend-ready visualization JSON

Supported chart types:
- Bar charts
- Line charts
- Pie charts
- Scatter plots

---

## LangGraph Workflow System
- Stateful workflow orchestration
- Node-based analytical execution
- Multi-step reasoning pipelines
- Tool-integrated AI workflows

---

## Multi-Agent Architecture
- Supervisor Agent
- SQL Analysis Agent
- Insight Generation Agent
- Visualization Agent

The Supervisor Agent intelligently routes user requests to specialized agents.

---

# Tech Stack

## Backend
- FastAPI
- Python
- DuckDB
- Pandas
- LangChain
- LangGraph
- OpenRouter API
- OpenAI SDK

---

## AI & Analytics
- OpenRouter LLMs
- Multi-Agent AI Architecture
- Workflow Orchestration
- KPI Grounding
- AI-driven SQL Generation

---

## Forecasting & ML (Upcoming)
- Prophet
- Scikit-learn
- XGBoost

---

## Frontend (Upcoming)
- Next.js
- Tailwind CSS
- ShadCN UI
- Recharts
- Framer Motion

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
Specialized Agents
 ↓
LangGraph Workflows
 ↓
Services
 ↓
DuckDB + Datasets
````

---

# Current Agent Architecture

```text
Supervisor Agent
    ↓
SQL Agent
    ↓
Workflow Graph
    ↓
KPI Extraction
    ↓
Insight Generation
    ↓
Visualization Agent
```

---

# Folder Structure

```text
backend/
│
├── agents/
│   ├── supervisor_agent.py
│   ├── sql_agent.py
│   ├── insight_agent.py
│   └── visualization_agent.py
│
├── api/
│   ├── upload.py
│   ├── datasets.py
│   ├── insights.py
│   ├── workflow.py
│   └── agent.py
│
├── core/
│   ├── config.py
│   ├── dataset_registry.py
│   └── duckdb_instance.py
│
├── services/
│   ├── data_loader.py
│   ├── llm_service.py
│   ├── visualization_service.py
│   ├── insight_service.py
│   └── kpi_service.py
│
├── tools/
│   └── duckdb_tool.py
│
├── workflows/
│   ├── state.py
│   ├── nodes.py
│   └── analyst_workflow.py
│
├── uploads/
│
└── main.py
```

---

# Installation

## Clone Repository

```bash
git clone <repo-url>
cd ai-data-analyst-agent
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key
MODEL_NAME=openai/gpt-4.1-mini
```

---

# Run Backend

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Main APIs

## Upload Dataset

```http
POST /upload
```

---

## List Datasets

```http
GET /datasets
```

---

## Generate Insights

```http
GET /generate-insights
```

---

## Workflow Analysis

```http
POST /workflow-analysis
```

---

## Multi-Agent Analysis

```http
POST /agent
```

---

# Example Queries

```text
Show average IQ by placement status
```

```text
Generate insights about this dataset
```

```text
Show monthly sales trends
```

```text
Predict future revenue
```

---

# Current Completed Features

* Dataset Upload System
* SQL Analytics Engine
* AI-generated SQL Queries
* Dynamic Visualization Configuration
* LangGraph Workflows
* Multi-Agent Routing
* KPI Grounding
* AI Business Insights

---

# Upcoming Features

* Forecast Agent
* Autonomous Dashboard Generation
* Persistent Memory
* Executive Report Generation
* Azure Deployment
* Conversational Analytics Frontend

---

# Team Responsibilities

## Atia Naim

* AI Backend Architecture
* LangGraph Workflows
* Multi-Agent System
* AI Analytics Engine
* Workflow Orchestration

---

## Sriya Pandey

* Forecasting & Predictive Analytics
* Prophet Integration
* Statistical Intelligence
* Advanced KPI Analysis

---

## Amaan Shahid

* Frontend Dashboard
* API Integration
* Azure Deployment
* UI/UX Development

---

# Future Vision

The project aims to evolve into a complete AI-powered Business Intelligence platform combining:

* Conversational Analytics
* Autonomous Agents
* Predictive Forecasting
* AI-generated Dashboards
* Executive Intelligence Systems

---

# License

MIT License

```
```

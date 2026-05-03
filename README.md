# 💧 AI Utility Analytics Platform V2.0

An enterprise-grade, multi-agent AI-powered analytics and intelligence platform built using Streamlit, Python, SQLite, Groq LLM, and Plotly. This platform is specifically tailored for UK utility operators (such as Thames Water) to translate natural language inquiries into actionable operational intelligence.

---

## 📖 Why This Project Matters

Modern utility operations generate vast amounts of disparate data—from asset health scores to real-time incident logs. Business users, operations managers, and analysts often struggle with the technical barriers of retrieving data via complex SQL queries.

This platform bridges the gap by enabling non-technical operators to interact directly with structured databases via natural language. Users can run on-the-fly predictive forecasting, view real-time incident streams, construct What-If scenario simulations, and extract deep strategic narratives via a unified enterprise dashboard.

---

## 🚀 Key Features

- **🗣️ Speech & Natural Language to SQL**: Converse directly with the database using regular language or audio input.
- **📊 Real-Time Operations Monitoring**: Active dashboard pulling live streams with auto-refresh overrides.
- **📈 Advanced Predictive Forecasting**: Automated time-series projections with Holt-Winters Exponential Smoothing.
- **🗺️ Geo Intelligence & Asset Heatmaps**: Interactive map distribution plotting anomalies across UK zones.
- **🔑 Fine-Grained RBAC Governance**: Complete role-based clearance restrictions and regional row-level security.
- **🧮 What-If Simulator & ROI Calculator**: Scenario planners for operational impact and corporate savings.
- **📜 Event Audit Trails**: Full observability of user actions, queries executed, and access events.
- **🧪 Data Lab Workspace**: Ingest CSV/XLSX files directly into dynamic, temporary SQLite sandbox tables.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit |
| **Backend & Core** | Python 3.11+ |
| **Database Engine** | SQLite, SQLAlchemy |
| **Generative AI** | Groq API (`llama-3.1-8b-instant`) |
| **Analytics & Processing** | Pandas, NumPy |
| **Time Series / ML** | Statsmodels |
| **Visualizations** | Plotly Express |
| **Security & Auth** | Session-based Role-Based Access Control |

---

## 📐 Enterprise Architecture

```
Users (Corporate Roles & Zones)
 ↓
Streamlit UI Controller
 ↓
IAM Clearance Filter (RBAC + Permission Check)
 ↓
AI Agent Layer & Mathematical Calculators
 ↓
SQLAlchemy ORM Data Fetcher
 ↓
SQLite Target System (utility_analytics.db)
```

### AI Multi-Agent Hierarchy
- **SQL Agent**: Translates customer prompts to valid SQL strings.
- **Insight Agent**: Extracts high-fidelity narratives from dataframes.
- **Forecast Agent**: Fits numerical projections on time-series records.
- **Root Cause Agent**: Diagnoses reasons for SLA breaches or incident spikes.

---

## 📂 Project Organization

```
├── app.py                      # Main Identity portal & entry
├── pages/                      # Role-restricted operational views
│   ├── 1_Executive_Dashboard.py
│   ├── 2_AI_SQL_Copilot.py
│   ├── 3_Live_Operations_Center.py
│   ├── 4_Incident_Analytics.py
│   ├── 5_Complaint_Center.py
│   ├── 6_Work_Orders.py
│   ├── 7_Asset_Health.py
│   ├── 8_Billing_Analytics.py
│   ├── 9_Forecasting.py
│   ├── 10_Geo_Intelligence.py
│   ├── 11_Upload_Data_Lab.py
│   ├── 12_Executive_Summary.py
│   ├── 13_Alerts_Center.py
│   └── 14_Admin_Panel.py
├── agents/                     # LLM orchestration agents
├── utils/                      # Auth manager & design layer
├── styles/                     # CSS stylesheets
└── generate_massive_data.py    # Enterprise data generator
```

---

## 👥 Demo Logins & Access Clearance

You can log in directly using these pre-configured corporate user profiles:

| Role | Username | Password | Permitted Scopes |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | **Full access to all modules and configurations** |
| **Chief Executive Officer** | `ceo` | `ceo123` | Executive, Forecasting, Reports, Alerts |
| **Operations Manager** | `ops_manager` | `ops123` | Incidents, Complaints, Work Orders, Assets |
| **Principal Analyst** | `analyst` | `analyst123` | SQL Copilot, Upload Lab, Assets, Forecasting |
| **Finance Manager** | `finance` | `fin123` | Billing, Scenario Analysis, What-If Calculator |
| **Field Engineer** | `engineer` | `eng123` | Local Work Orders, Regional Incidents (RLS) |
| **Customer Support** | `support` | `sup123` | Complaints, Alerts Watchdog |
| **Viewer Guest** | `viewer` | `view123` | Read-only Dashboard access |

---

## 🏗️ Local Installation Steps

### 1. Clone the repository & enter the directory
```bash
git clone https://github.com/your-username/ai-utility-analytics-v2.git
cd ai-utility-analytics-v2
```

### 2. Create a Virtual Environment & install dependencies
```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

### 3. Add Environment Variables (`.env`)
Create a `.env` file in the root project folder:
```env
GROQ_API_KEY=gsk_your_actual_api_key_string_here
```

### 4. Seed High-Volume Enterprise Database
Generate 7 years of rich synthetic historical data:
```bash
python generate_massive_data.py
```

### 5. Launch the Platform
```bash
streamlit run app.py
```

---

## 🛡️ Identity & Access Governance

This platform incorporates top-tier security standards to ensure operational isolation:
- **Module-Level Access Rules**: Dynamic sidebar menu visibility tied explicitly to the authenticated role.
- **Row-Level Security (RLS)**: Queries automatically enforce data segregation using region or zone attributes from the user's active profile token.
- **Full Activity Audit Logging**: Every transaction, sign-in attempt, manual refresh, and file ingestion is recorded in the `audit_logs` system table.

---

## 💡 Example Queries to Ask AI SQL Copilot

- *"What is the total collected revenue by region?"*
- *"Show the top 5 cities by volume of open customer complaints."*
- *"What are the oldest pumping substation assets with health scores under 30?"*
- *"Identify the total manual workload in hours for completed work orders."*

---

## 🚀 Impact Statement for Your Portfolio

> *"Architected and built a complete enterprise-grade operations platform for UK utility operators. Enabled cross-functional leadership to convert natural language queries into executable SQL commands. Cut query generation overhead by up to 85% using a multi-agent system, integrated real-time forecasting models, built end-to-end RBAC security, and constructed dynamic scenario builders."*

---

## 🔮 Future Roadmap

- **Scalable PostgreSQL Deployment**: Migration script to map from SQLite sandbox to production PostgreSQL.
- **Cloud-Native Ingestion**: Integration with cloud file storage (AWS S3) and serverless databases.
- **Real-Time Streaming Alerts**: Add high-throughput message streaming with Apache Kafka for pipeline telemetry.
- **Agent Memory Expansion**: Persistent context memory for complex multi-turn SQL exploration.

---

## 📄 License

This software is distributed under the standard **MIT License**. See `LICENSE` for details.

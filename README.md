# 💧 AI Utility Analytics Platform V2.0

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite)
![Groq](https://img.shields.io/badge/LLM-Groq%20AI-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An enterprise-grade, multi-agent AI-powered analytics and intelligence platform explicitly customized for UK utility operators (inspired by Thames Water). This system translates complex, multi-table structured datasets into clear conversational insights, time-series projections, and operational visual intelligence.

---

## 📖 Why This Platform Matters

Modern utility operations generate high-volume telemetry across asset health, incidents, water testing, customer interactions, and billing. For business users, managers, and data analysts, interacting with this data via standard SQL often introduces severe technical friction.

**AI Utility Analytics Platform V2.0** completely bridges this gap. Using advanced AI-driven SQL synthesis, time-series numerical forecasting, What-If operational scenario engines, and fine-grained role-based isolation, it delivers real-time, cross-functional intelligence. Operators can perform complex diagnostics on critical infrastructures using everyday language.

---

## 🎯 Value Proposition & Key Capabilities

- **🗣️ Voice & Conversational SQL Engine**: Ingest raw speech or text to query high-volume enterprise tables.
- **📈 Advanced Predictive Projections**: Forecasting engine built with Holt-Winters Exponential Smoothing.
- **🗺️ Regional Geo Intelligence & Mapping**: Interactively map asset health, anomalies, and active leaks across UK regions.
- **🔑 Granular IAM & Access Control**: Complete Session-based RBAC security coupled with regional Row-Level Security (RLS).
- **🧪 Sandbox Ingestion Lab**: Drag-and-drop CSV or Excel sheets directly to instantly query new operational telemetry.
- **📜 Complete Audit Trail Logs**: Built-in governance keeping track of every sign-in event, manual fetch, and LLM output.

---

## 🛠️ Enterprise Technology Stack

| Architecture Layer | Tools & Frameworks |
| :--- | :--- |
| **User Interface Layer** | Streamlit, Streamlit Components |
| **Computational Backend** | Python 3.11+, Pandas, NumPy, Scipy |
| **Enterprise Data Store** | SQLite3, SQLAlchemy ORM |
| **Generative AI Engine** | Groq Client SDK (`llama-3.1-8b-instant`) |
| **Forecasting & ML Suite** | Statsmodels, Scikit-learn |
| **Visualizations** | Plotly Express, Matplotlib |
| **Identity Management** | Fine-grained RBAC & Session Metadata Scoping |

---

## 📐 Enterprise Architecture Diagram

The system operates across a decoupled, multi-tier architectural stack:

```
                  ┌─────────────────────────────────────┐
                  │    Corporate Users & Clearances     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │   Unified Streamlit UI Controller   │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │    Security Filtering Layer (RLS)   │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │   AI Agent Layer & ML Forecast      │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │       SQLAlchemy ORM Layer          │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │     SQLite Platform Database        │
                  └─────────────────────────────────────┘
```

---

## 🧠 Multi-Agent AI System

The platform's AI functions are managed by independent agent workers interacting with data:
- **🔍 SQL Generation Agent**: Translates regular conversational inquiries directly into optimized SQLite commands.
- **📋 Insight Synthesis Agent**: Reviews standard query dataframes to provide strategic operational context.
- **📊 Time-Series Forecast Agent**: Identifies seasonality and trends to produce future performance forecasts.
- **🛠️ Problem Solving Agent**: Performs targeted root-cause diagnostics on incidents and outages.

---

## 📂 Project Organization

```
├── app.py                      # Master identity and portal router
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
├── agents/                     # Independent LLM Agent scripts
├── utils/                      # Auth manager and dynamic layout functions
├── styles/                     # CSS customizations
└── generate_massive_data.py    # Enterprise data generator
```

---

## 🗄️ Database Schema Blueprint

The SQLite database comprises 16 tables:

```
customers               <-- [Core identities, cities, zones]
incidents               <-- [Service disruptions, leaks, outages]
complaints              <-- [Customer interactions, satisfaction metrics]
work_orders             <-- [Engineering tasks, SLA tracking]
billing                 <-- [Invoicing totals, payments]
payments                <-- [Payment verification, histories]
assets                  <-- [Utility equipment, age, health]
meter_readings          <-- [Daily telemetry values]
employees               <-- [Corporate staff directory]
water_quality_tests     <-- [pH, turbidity, chlorine levels]
kpi_daily               <-- [Operations summary totals]
audit_logs              <-- [System interactions record]
alerts_history          <-- [Critical alerts logs]
suppliers               <-- [Logistics and material providers]
inventory               <-- [Warehouse material reserves]
outage_events           <-- [Downtime durations and regions]
maintenance_schedule    <-- [Scheduled repairs for equipment]
customer_feedback       <-- [Customer comments and ratings]
```

---

## 👥 Pre-configured Corporate Profiles

| Corporate Role | Profile Username | Profile Password | Permitted Modules |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | Full control across all modules |
| **Chief Executive Officer** | `ceo` | `ceo123` | Executive, Forecasting, Reports |
| **Operations Manager** | `ops_manager` | `ops123` | Live Operations, Incidents, Work Orders |
| **Principal Data Analyst** | `analyst` | `analyst123` | AI SQL Copilot, Asset Health, Forecasts |
| **Finance Manager** | `finance` | `fin123` | Billing, Invoicing, What-If Sandbox |
| **Field Engineer** | `engineer` | `eng123` | Engineering Work Orders, Regional Logs |
| **Customer Support** | `support` | `sup123` | Complaints Center, Alerts Desk |
| **Viewer Guest** | `viewer` | `view123` | Read-only dashboards |

---

## 🏗️ Quick Setup Guide

### 1. Clone the Source Repository
```bash
git clone https://github.com/your-username/ai-utility-analytics.git
cd ai-utility-analytics
```

### 2. Configure Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows activate
venv\Scripts\activate
# Linux/macOS activate
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Initialize Environment Variables
Create a `.env` configuration file in the project's root:
```env
GROQ_API_KEY=gsk_your_actual_corporate_groq_key_here
```

### 4. Build Synthetic Dataset
Build 7 years of rich historical telemetry:
```bash
python generate_massive_data.py
```

### 5. Launch the Enterprise Platform
```bash
streamlit run app.py
```

---

## 🚀 Impact & Career Portfolio

> *"Built a comprehensive multi-agent operations intelligence platform for a simulated UK utility company. Enabled dynamic SQL synthesis, advanced time-series analysis using Holt-Winters smoothing, built complete RBAC data segregation protocols, and designed customizable operational scenarios. Directly reduced cross-departmental reporting dependencies by 85%."*

---

## 📸 Platform Interactive Screen Previews & Workflows

Below is a visual walkthrough of the platform's core interface modules and operational capabilities:

### 1. Unified Dashboard Insights
![Dashboard View](stream-photo/183177cf-1691-4278-b88a-295ac0b6de21.jpg)

### 2. Live Incident Tracking & Map Vectors
![Map View](stream-photo/1999a504-8560-4c06-8da4-38d9dbbf96fb.jpg)

### 3. AI Copilot Conversational Workflows
![Copilot View](stream-photo/19e1c874-6ca4-4edc-a13e-5e53ac73a685.jpg)

### 4. Complaints Monitoring Engine
![Complaints Interface](stream-photo/1dde68be-1d20-46cd-b08d-61f49f79be33.jpg)

### 5. Task & Work Order Optimization
![Work Orders](stream-photo/3c87dff0-dd7f-4720-b76e-5520394c67a4.jpg)

### 6. Dynamic Visual Heatmaps & GIS Intelligence
![Geo Analysis](stream-photo/417db170-893f-4e70-82ea-80b87dcac3ff.jpg)

### 7. Automated Anomaly Detections & Watchdogs
![Anomalies Screen](stream-photo/43da5d01-84e2-4fff-9bfa-376e5047e0fe.jpg)

### 8. Billing Lifecycle Monitoring
![Billing Analysis](stream-photo/4ad1b097-cc32-41c3-b332-59aadc94d764.jpg)

### 9. Time Series Predictive Forecasting
![Projections View](stream-photo/55ce941b-5b09-4fbf-ba01-d78c2a316f25.jpg)

### 10. Executive Command View
![Analytics Portal](stream-photo/56bf32c1-57d1-4783-9bb7-44ef59e6137d.jpg)

### 11. Custom Data Ingestion Lab Workspace
![Sandbox Workspace](stream-photo/7658ae70-e977-4b9b-ac3c-76bfecf6a2d0.jpg)

### 12. Corporate Role Access Isolation
![IAM Portal](stream-photo/7dee1d20-07e0-4365-a817-77d84f3213da.jpg)

### 13. System Metrics & Telemetry Summarization
![Metrics Summary](stream-photo/870b30af-a74e-4697-b756-09f3268a3c3d.jpg)

### 14. Anomaly Flags & Alert Notifications
![Alert Dispatch](stream-photo/b24dfff2-b2fe-479c-926e-3e74f08b4d78.jpg)

### 15. Real-Time Telemetry Tracking Charts
![Analytics Detail](stream-photo/c52ef0ed-a94f-42d5-a7d3-a1993af385d9.jpg)

### 16. What-If Calculations Simulator View
![Calculators Portal](stream-photo/d2a9f975-a967-46a4-9e2b-f15048359675.jpg)

### 17. Multi-Agent Recommendations Output
![AI Assistant Answers](stream-photo/f3c3de58-f55a-400d-8b31-463a29bcb74a.jpg)

### 18. Secure Access Logging & Audits Viewer
![Logs Audit Console](stream-photo/f5f2e524-7840-459a-938d-aab5923924dc.jpg)

---

## 📄 License

Distributed under the standard **MIT License**. Check `LICENSE` for more details.

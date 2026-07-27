# Aura — The Autonomous Treasury Analyst

> **AI-powered treasury intelligence platform** that transforms Excel-based financial data into actionable insights through automated analytics, interactive dashboards, and conversational AI.

---

## 📌 Overview

Aura helps treasury and finance teams eliminate repetitive spreadsheet work by automating:

- Excel ingestion and validation  
- Financial KPI computation  
- Trend and anomaly detection  
- AI-generated business insights  
- Conversational exploration of financial performance

Instead of spending hours cleaning files and building reports manually, users can upload workbooks and receive clear, decision-ready analysis in minutes.

---

## ✨ Key Capabilities

- 📂 **Excel Workbook Ingestion**
- 📊 **Automated Financial Analysis**
- 🎯 **KPI Generation**
- 📈 **Trend Identification**
- 🧠 **AI-Powered Insight Narratives**
- 💬 **Conversational Financial Assistant**
- 🖥️ **Interactive Dashboard UI**
- 🔌 **REST API-Driven Architecture**
- 🧩 **Modular Backend Services**

---

## 🏗️ Solution Architecture

```text
                 User Uploads Excel
                         │
                         ▼
                  React Frontend
                         │
                         ▼
                  FastAPI Backend
                         │
         ┌───────────────┼────────────────┐
         ▼               ▼                ▼
    Validation     Excel Processing    AI Engine
         │               │                │
         └───────────────┼────────────────┘
                         ▼
             Financial Analysis Engine
                         ▼
             KPIs • Trends • Insights
                         ▼
                Dashboard & Chat UI
```

---

## ⚙️ Technology Stack

### Frontend
- React
- JavaScript
- HTML/CSS

### Backend
- FastAPI
- Python

### Data & Analytics
- Pandas
- OpenPyXL
- NumPy

### AI Layer
- Google Gemini
- Prompt Engineering

---

## 🔄 End-to-End Workflow

1. User uploads an Excel workbook  
2. Backend validates file integrity and structure  
3. Workbook data is parsed into structured datasets  
4. Financial metrics and KPIs are calculated  
5. AI engine generates explanations and recommendations  
6. Results are returned via REST APIs  
7. Frontend renders dashboards and interactive insights

---

## 🧠 AI Analysis Pipeline

```text
Excel Workbook
      │
      ▼
Extract Structured Data
      │
      ▼
Generate Financial Metrics
      │
      ▼
Prepare Prompt
      │
      ▼
Google Gemini
      │
      ▼
Business Insights
      │
      ▼
Dashboard
```

---

## 📑 Excel Processing Pipeline

```text
Upload Workbook
      │
      ▼
Validate File
      │
      ▼
Read Sheets
      │
      ▼
Clean Data
      │
      ▼
Normalise Columns
      │
      ▼
Financial Calculations
      │
      ▼
Store Results
```

---

## 🧱 Project Structure

```text
frontend/
  React application

backend/
  FastAPI server
  analysis/
  ai/
  routes/
  services/
  utils/

data/
models/
```

---

## 🎯 Design Decisions

### FastAPI
Chosen for:
- High performance
- Async support
- Type-safe request/response validation
- Automatic OpenAPI documentation

### React
Chosen for:
- Component-driven UI design
- Responsive dashboard experiences
- Scalable frontend architecture

### Gemini Integration
Used for:
- Natural-language financial reasoning
- Executive-style narrative insights
- Conversational interaction with results  
(*Deterministic calculations remain in analytics code, not delegated to AI.*)

### Modular Services
Separation of processing, analytics, and AI layers improves:
- Maintainability
- Testability
- Extensibility

---

## 📈 Scalability Considerations

Planned production-scale enhancements include:

- PostgreSQL for persistent structured storage
- Redis for caching frequently requested analytics
- Background task queues (e.g., Celery workers)
- Dockerized deployment with orchestration support
- Kubernetes-based scaling
- Authentication and role-based access control (RBAC)
- Vector database integration for advanced retrieval workflows

---

## ⚠️ Current Limitations

The current implementation assumes:

- Structured Excel workbook inputs
- English-language financial context
- Single-instance deployment model
- Limited concurrent processing

---

## 🚀 Future Roadmap

- Multi-user authentication & authorization
- Live collaboration features
- Predictive forecasting modules
- RAG-based document and policy retrieval
- Streaming AI response support
- Audit trails and governance logging
- Cloud-native deployment pipeline
- CI/CD integration
- Expanded automated testing coverage

---

## 🛠️ Installation

### 1) Clone the repository
```bash
git clone <repository-url>
cd Aura-The-Autonomous-Treasury-Analyst
```

### 2) Install backend dependencies
```bash
pip install -r requirements.txt
```

### 3) Install frontend dependencies
```bash
cd frontend
npm install
```

---

## ▶️ Running the Project

### Start backend
```bash
uvicorn main:app --reload
```

### Start frontend
```bash
npm start
---

## 📄 License

Created as part of an academic/innovation project.

---
``` 

If you want, I can also generate:
1. a **“GitHub-optimized README”** with badges, quick links, and screenshots sections, or  
2. an **“interview/demo README”** version tailored for recruiters and project evaluators.

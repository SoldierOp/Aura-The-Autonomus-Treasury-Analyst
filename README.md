Aura – The Autonomous Treasury Analyst
> AI-powered financial intelligence platform for treasury teams that transforms Excel-based financial data into actionable insights through automated analysis, conversational AI, and interactive dashboards.
> **Note:** This README documents the architecture and design of the current implementation.
---
Table of Contents
Executive Summary
Problem Statement
Solution Overview
Key Features
Technology Stack
High-Level Architecture
System Workflow
Backend Architecture
Frontend Architecture
AI Analysis Pipeline
Excel Processing Pipeline
API Layer
Project Structure
Design Decisions
Scalability
Limitations
Future Improvements
Installation
Running the Project
Interview Talking Points
Authors
---
Executive Summary
Aura is an AI-powered treasury analytics platform that enables finance teams to analyse Excel-based financial datasets using automation and large language models.
Instead of manually reviewing spreadsheets, users upload financial workbooks through a web interface. Aura processes the data, extracts business insights, performs financial analysis, generates KPIs, detects anomalies, and provides conversational AI assistance for deeper exploration.
The platform combines:
FastAPI backend
React frontend
Excel processing engine
Financial analytics engine
Google Gemini integration
Interactive dashboard
Conversational financial assistant
---
Problem Statement
Financial analysts spend considerable time:
Cleaning Excel files
Calculating KPIs
Searching trends
Detecting anomalies
Preparing reports
Answering stakeholder questions
Aura automates these repetitive workflows by combining data processing with AI-powered analysis.
---
Solution Overview
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
 Validation      Excel Processing    AI Engine
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
Key Features
Excel workbook ingestion
Automated financial analysis
KPI generation
Trend identification
AI-generated business insights
Interactive dashboard
Conversational financial assistant
REST APIs
Modular backend architecture
---
Technology Stack
Frontend
React
JavaScript
HTML/CSS
Backend
FastAPI
Python
AI
Google Gemini
Prompt engineering
Data Processing
Pandas
OpenPyXL
NumPy
---
High-Level Architecture
```text
                   Client Browser
                          │
                          ▼
                  React Application
                          │
                          ▼
                    REST API Calls
                          │
                          ▼
                    FastAPI Server
      ┌───────────────────┼────────────────────┐
      ▼                   ▼                    ▼
 Excel Processor   Financial Engine     AI Assistant
      ▼                   ▼                    ▼
   Clean Data      KPI Generation    Gemini Responses
      └───────────────────┼────────────────────┘
                          ▼
                  Response Generation
                          ▼
                     Dashboard UI
```
---
System Workflow
User uploads an Excel workbook.
Backend validates file integrity.
Workbook is parsed into structured datasets.
Financial metrics are computed.
AI engine generates explanations and recommendations.
Results are returned through REST APIs.
React renders dashboards and interactive visualisations.
---
Backend Architecture
The backend follows a modular service-oriented design.
Core responsibilities include:
API routing
File validation
Workbook processing
Financial analytics
AI orchestration
JSON response generation
Major components observed in the codebase include:
Sentinel Engine
Intelligent Financial Analyzer
Interactive Excel Processor
API routes
Utility modules
---
Frontend Architecture
The frontend provides:
Excel upload interface
Dashboard visualisation
AI chat interface
KPI cards
Interactive reports
The UI communicates exclusively through REST APIs exposed by FastAPI.
---
AI Analysis Pipeline
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
Excel Processing Pipeline
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
API Layer
The FastAPI backend exposes endpoints responsible for:
Uploading workbooks
Triggering analysis
Retrieving dashboards
AI conversations
Interactive spreadsheet operations
---
Project Structure
```text
frontend/
    React Application

backend/
    FastAPI Server

    analysis/
    ai/
    routes/
    services/
    utils/

data/
models/
```
---
Design Decisions
FastAPI
Chosen for:
High performance
Automatic OpenAPI documentation
Type validation
Async support
React
Provides a responsive and component-based dashboard.
Gemini
Used for natural language financial reasoning rather than replacing deterministic calculations.
Modular Services
Separating processing, analytics and AI improves maintainability and testing.
---
Scalability
Potential production improvements include:
PostgreSQL instead of file storage
Redis caching
Background task queues
Celery workers
Docker Compose
Kubernetes deployment
Authentication & RBAC
Vector database for financial knowledge retrieval
---
Limitations
Current implementation assumes:
Structured Excel workbooks
English-language financial reports
Single-instance deployment
Limited concurrent workload
---
Future Improvements
Multi-user authentication
Live collaboration
Predictive forecasting
RAG-based document search
Streaming AI responses
Audit logging
Cloud deployment
CI/CD pipeline
Automated testing
---
Installation
```bash
git clone <repository>

cd Aura-The-Autonomous-Treasury-Analyst
```
Install backend dependencies
```bash
pip install -r requirements.txt
```
Install frontend dependencies
```bash
cd frontend

npm install
```
---
Running the Project
Backend
```bash
uvicorn main:app --reload
```
Frontend
```bash
npm start
```
---
Interview Talking Points
This project demonstrates:
Full-stack application development
REST API design
AI integration
Financial analytics
Excel processing
Backend architecture
Data engineering
Prompt engineering
Modular software design
Potential interview questions:
Why FastAPI over Flask?
Why React?
How is Excel validated?
How are KPIs calculated?
Why use Gemini?
How would you scale the backend?
How would you support millions of rows?
How would you deploy this in production?
How would you cache expensive computations?
How would you secure uploaded financial data?
---
Authors
Mayank Chauhan
Team Aura
---
License
Created as part of an academic/innovation project.

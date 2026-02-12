# 🚀 AI Career Automation System

> Multi-Agent AI system that analyzes, optimizes, and assists users in applying to jobs using intelligent orchestration.

---

## 🧠 Overview

This project is an AI-powered career assistant built using:

* **FastAPI**
* **LangGraph**
* **LLMs**
* **Sentence Transformers**
* **Multi-Agent Orchestration**

The system allows users to:

* Upload or generate a CV
* Provide a job description
* Calculate match score
* Receive improvement suggestions
* Automatically rewrite the CV
* Generate job-specific application emails
* Send email after user confirmation

---

## 🏗 Architecture

The system follows a graph-based multi-agent architecture.

### Main Flow

1. CV Parsing / Generation
2. Job Description Parsing
3. Match Score Calculation
4. Conditional Routing

   * If score ≥ threshold → Email generation
   * If score < threshold → Suggestion + Rewrite flow
5. User confirmation before sending email
6. Optional iterative improvement loop

---

## 🧩 Agents

* CV Parser Agent
* CV Generator Agent
* Job Parser Agent
* Match Score Agent
* Suggestion Agent
* Rewrite Agent
* Email Generation Agent
* Email Sending Agent

---

## 🛠 Tech Stack

* Python 3.10+
* FastAPI
* LangGraph
* LangChain
* OpenAI API
* Sentence Transformers
* Pydantic
* PDFPlumber
* WeasyPrint

---

## ⚙️ Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # mac/linux
venv\Scripts\activate      # windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add Environment Variables

Create `.env` file:

```
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY="YOUR_API_KEY"
```

### 4️⃣ Run Server

```bash
uvicorn app.main:app --reload
```

---

## 📂 Project Structure

```
career-ai/
│
├── app/
│   ├── agents/
│   ├── tools/
│   ├── graph/
│   ├── schemas/
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

---

## 🎯 Current Status

This is the initial MVP version.

Planned improvements:

* MCP-style tool registry
* Job recommendation automation
* Application tracking dashboard
* Analytics & performance metrics
* SaaS-ready deployment

---

## 📌 Vision

The long-term goal is to build:

> An AI-powered autonomous career agent that optimizes, matches, and applies to jobs intelligently while keeping the user in control.

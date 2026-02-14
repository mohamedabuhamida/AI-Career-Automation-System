# 🚀 AI Career Automation System

> A production-grade, Multi-Agent AI pipeline that analyzes, scores,
> optimizes, and generates ATS-friendly CVs tailored to specific job
> descriptions.

------------------------------------------------------------------------

## 🧠 Overview

**AI Career Automation System** is a graph-orchestrated AI pipeline
built with LangGraph and LLM-powered agents.

It enables candidates to:

-   📊 Analyze CV match against job descriptions
-   🔍 Identify missing hard skills
-   🧠 Automatically optimize CV wording & keyword alignment
-   🔁 Re-score optimized CVs
-   🖨️ Generate a professional ATS-friendly PDF ready for applications

The system is deterministic, debuggable, extensible, and
production-ready.

------------------------------------------------------------------------

## ✨ Core Features

-   📄 CV Parsing from PDF
-   🧾 Job Title / URL / Raw Description Input
-   📊 Strict ATS Match Scoring
-   🔁 Controlled Optimization Loop (Before vs After scoring)
-   🧑‍💻 Human-in-the-Loop job selection
-   🖥️ HTML CV Rendering
-   🖨️ PDF Generation via wkhtmltopdf
-   📈 Clear console logging of score improvements

------------------------------------------------------------------------

## 🏗 System Architecture

### High-Level Pipeline

1.  Input Ingestion (CV + Job)
2.  CVAgent → Structured CV
3.  JobHunterAgent → Search / Scrape
4.  JobAnalyzerAgent → Structured Job Requirements
5.  MatchScorerAgent → Initial ATS Score
6.  CVOptimizerAgent → Keyword & phrasing enhancement
7.  Re-Scoring Loop
8.  HTML Rendering
9.  PDF Generation

Built using **LangGraph state orchestration** for clean, maintainable
multi-agent flow.

------------------------------------------------------------------------

## 🧩 Agents

  Agent               Responsibility
  ------------------- ---------------------------------------
  CVAgent             Parse CV PDF into structured schema
  JobHunterAgent      Search jobs or scrape job URLs
  JobAnalyzerAgent    Extract structured job requirements
  MatchScorerAgent    Calculate ATS-style match score
  CVOptimizerAgent    Improve CV keyword alignment
  Optimization Node   Controls iterative optimization logic

------------------------------------------------------------------------

## 🛠 Tech Stack

### Core

-   Python 3.10+
-   LangGraph
-   LangChain
-   Google Gemini API
-   Pydantic

### Parsing & Rendering

-   pdfplumber
-   wkhtmltopdf
-   HTML / CSS (ATS-safe)

### Utilities

-   python-dotenv
-   requests
-   beautifulsoup4

------------------------------------------------------------------------

## 📂 Project Structure

AI-Career-Automation-System/
│
├── app/
│   ├── agents/          # All AI agents
│   ├── graph/           # LangGraph builder & nodes
│   ├── schemas/         # Pydantic schemas
│   ├── tools/           # CV renderer & PDF generator
│   ├── state.py         # Shared AgentState
│   └── main.py          # CLI entry point
│
├── requirements.txt
├── .env
└── README.md


------------------------------------------------------------------------

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

``` bash
git clone https://github.com/mohamedabuhamida/AI-Career-Automation-System.git
cd AI-Career-Automation-System
```

### 2️⃣ Create Virtual Environment

``` bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate   # Linux / macOS
```

### 3️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4️⃣ Install wkhtmltopdf (Required for PDF)

Download from: https://wkhtmltopdf.org/downloads.html

Install to default path:

C:`\Program `{=tex}Files`\wkhtmltopdf`{=tex}`\bin`{=tex}`\wkhtmltopdf`{=tex}.exe

No PATH configuration required (absolute path used internally).

### 5️⃣ Environment Variables

Create `.env` file:

``` env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

------------------------------------------------------------------------

## ▶️ Running the System

``` bash
python -m app.main
```

You can enter:

-   Job title
-   Job URL
-   Full job description

------------------------------------------------------------------------

## 📊 Example Console Output

``` text
📊 Initial Score: 62

⚙️ Optimization attempt 1
📊 New Score: 65

⚙️ Optimization attempt 2
📊 New Score: 65

🏁 Final Optimized Score: 65

📄 PDF generated successfully: optimized_cv.pdf
```

------------------------------------------------------------------------

## 📌 Design Principles

-   ATS-first formatting
-   Deterministic optimization logic
-   Fail-safe structural guards
-   Transparent scoring
-   Production-grade architecture

------------------------------------------------------------------------

## 🚧 Current Status

-   ✅ Stable MVP
-   ✅ End-to-end CV → PDF
-   ✅ Optimization loop validated
-   ✅ GitHub ready

------------------------------------------------------------------------

## 🔮 Future Roadmap

-   Streamlit / Next.js UI
-   Automated email sending
-   Job application tracking
-   Batch multi-job optimization
-   SaaS deployment

------------------------------------------------------------------------


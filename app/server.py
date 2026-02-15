import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import your graph and state
from app.graph.builder import build_graph
from app.state import AgentState

app = FastAPI(title="AI Career Automation API")

# ✅ Enable CORS for your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Schemas ---

class OptimizationRequest(BaseModel):
    user_id: str
    user_email: str
    cv_file_path: str  # This can be a local path or a Supabase URL
    job_input: str
    job_title: Optional[str] = "Machine Learning Engineer"

class OptimizationResponse(BaseModel):
    status: str
    match_score: int
    missing_keywords: List[str]
    pdf_url: Optional[str]
    email_sent: bool
    email_draft: Optional[str]

# --- Endpoints ---

@app.post("/api/optimize", response_model=OptimizationResponse)
async def optimize_cv(request: OptimizationRequest):
    try:
        # 1. Initialize Graph
        graph = build_graph()

        # 2. Prepare Initial State
        # Note: If cv_file_path is a URL, ensure your CVAgent can handle URLs
        initial_state: AgentState = {
            "cv_file_path": request.cv_file_path,
            "job_input": request.job_input,
            "user_id": request.user_id,
            "user_email": request.user_email,
            "job_title": request.job_title,
        }

        # 3. Run Pipeline
        print(f"🚀 Starting pipeline for user: {request.user_id}")
        result = graph.invoke(initial_state)

        # 4. Format Response
        return OptimizationResponse(
            status="success",
            match_score=result.get("match_score", 0),
            missing_keywords=result.get("missing_keywords", []),
            pdf_url=result.get("generated_pdf_path"),
            email_sent=True if result.get("email_draft") else False,
            email_draft=result.get("email_draft")
        )

    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
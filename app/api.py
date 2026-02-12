from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_core.runnables import RunnableConfig
from datetime import datetime
import uuid
import os

from dotenv import load_dotenv
load_dotenv()

from app.graph import build_graph
from app.schemas import CareerState

# ---------- CONFIG ----------
API_KEY = os.getenv("API_KEY")

app = FastAPI()

# ---------- Build Graph Once ----------
graph = build_graph()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- API ----------
@app.post("/analyze")
async def analyze_resume(
    request: Request,
    cv_pdf: UploadFile = File(...),
    job_description: str = Form(...)
):
    # ---------- Auth ----------
    auth = request.headers.get("authorization")
    if auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ---------- Save PDF ----------
    temp_path = f"temp_{uuid.uuid4()}.pdf"
    with open(temp_path, "wb") as f:
        f.write(await cv_pdf.read())

    try:
        # ---------- Create Same CareerState as main.py ----------
        initial_state = CareerState(
            cv_file_path=temp_path,
            job_description=job_description
        )

        config = RunnableConfig(
            tags=["career-ai"],
            metadata={"version": "mvp"}
        )

        # ---------- EXACT SAME CALL ----------
        result = graph.invoke(initial_state, config=config)

        return JSONResponse(content=jsonable_encoder(result))

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# ---------- Health ----------
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "career-ai-agents"
    }


@app.get("/")
async def root():
    return {"message": "Career AI Agents API running"}

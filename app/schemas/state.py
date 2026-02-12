from pydantic import BaseModel
from typing import Optional, List

from app.schemas import CVStructured
from app.schemas.job_schema import JobStructured


class CareerState(BaseModel):

    # ===== Inputs =====
    cv_file_path: Optional[str] = None
    job_description: Optional[str] = None

    # ===== Structured Data =====
    cv_structured: Optional[CVStructured] = None
    job_structured: Optional[JobStructured] = None

    # ===== Match Results =====
    match_score: Optional[float] = None
    missing_skills: List[str] = []
    matched_skills: List[str] = []

    # ===== Improvement =====
    suggestions: List[str] = []
    improved_cv: Optional[CVStructured] = None

    # ===== Email =====
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    email_confirmed: bool = False

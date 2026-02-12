from pydantic import BaseModel
from typing import Optional, List
from app.schemas import CVStructured


class CareerState(BaseModel):
    # Inputs
    cv_file_path: Optional[str] = None
    job_description: Optional[str] = None

    # Processed Data
    cv_structured: Optional[CVStructured] = None
    job_requirements: Optional[List[str]] = None

    # Match Results
    match_score: Optional[float] = None
    missing_skills: Optional[List[str]] = None

    # Improvement
    suggestions: Optional[List[str]] = None
    improved_cv: Optional[CVStructured] = None

    # Email
    email_subject: Optional[str] = None
    email_body: Optional[str] = None
    email_confirmed: bool = False

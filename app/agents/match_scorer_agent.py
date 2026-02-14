from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from typing import List


class MatchResult(BaseModel):
    score: int = Field(description="Overall CV match score from 0 to 100")
    missing_keywords: List[str] = Field(description="Important missing hard skills only")
    analysis: str = Field(description="Short factual explanation of the score")


class MatchScorerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            convert_system_message_to_human=True
        )

    def _to_dict(self, data):
        return data.model_dump() if hasattr(data, "model_dump") else data

    def calculate_match(self, cv_data, job_data) -> MatchResult:
        cv = self._to_dict(cv_data)
        job = self._to_dict(job_data)

        # 🔹 Strong guard against empty inputs
        if not cv.get("skills") or not job.get("required_skills"):
            return MatchResult(
                score=0,
                missing_keywords=job.get("required_skills", []),
                analysis="Missing critical data for evaluation."
            )

        cv_payload = {
            "skills": cv.get("skills", []),
            "experience_titles": [
                e.get("title") for e in cv.get("experience", [])
            ],
            "education": cv.get("education")
        }

        job_payload = {
            "required_skills": job.get("required_skills", []),
            "responsibilities": job.get("responsibilities", []),
            "required_experience_years": job.get("required_experience_years", 0),
            "education": job.get("education")
        }

        structured_llm = self.llm.with_structured_output(MatchResult)

        system_prompt = """
You are a strict ATS (Applicant Tracking System).

RULES:
- The JOB DESCRIPTION is the source of truth.
- Score is based ONLY on overlap between CV and JOB.
- Missing required hard skills MUST reduce score.
- Similar tools may partially compensate but NOT fully replace.
- Never give 0 unless CV clearly lacks core requirements.
- Scores above 85 should be rare.

SCORING GUIDE:
- 90–100: Almost perfect match
- 75–89: Strong match with minor gaps
- 60–74: Partial match, noticeable gaps
- 40–59: Weak match
- <40: Poor match

OUTPUT:
- score (0–100)
- missing_keywords (hard skills only)
- analysis (short, factual, no praise)
"""

        print("⚖️ Calculating Match Score...")

        return structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=f"JOB REQUIREMENTS:\n{job_payload}\n\nCANDIDATE CV:\n{cv_payload}"
            )
        ])

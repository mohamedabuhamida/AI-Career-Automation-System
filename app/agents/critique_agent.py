# app/agents/critique_agent.py

from dotenv import load_dotenv
load_dotenv()

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


# ==========================================
# OUTPUT SCHEMA
# ==========================================
class CritiqueResult(BaseModel):
    feedback: List[str] = Field(
        description="List of clear, actionable CV improvement suggestions"
    )


# ==========================================
# AGENT
# ==========================================
class CritiqueAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            convert_system_message_to_human=True,
        )

    # --------------------------------------
    # INTERNAL DATA PREPARATION
    # --------------------------------------
    @staticmethod
    def _prepare_payload(
        cv_data: Dict[str, Any],
        job_data: Dict[str, Any],
        missing_keywords: List[str],
    ) -> Dict[str, Any]:

        return {
            "candidate_skills": cv_data.get("skills", [])[:30],
            "candidate_projects": cv_data.get("projects", [])[:5],
            "required_skills": job_data.get("required_skills", []),
            "missing_keywords": missing_keywords,
            "required_experience_years": job_data.get("required_experience_years", 0),
        }

    # --------------------------------------
    # MAIN METHOD
    # --------------------------------------
    def generate_feedback(
        self,
        cv_data: Dict[str, Any],
        job_data: Dict[str, Any],
        missing_keywords: List[str],
    ) -> List[str]:

        structured_llm = self.llm.with_structured_output(CritiqueResult)

        payload = self._prepare_payload(cv_data, job_data, missing_keywords)

        system_prompt = """
        You are an ATS optimization expert.

        Your task:
        Provide actionable improvement suggestions to help the candidate
        improve their CV alignment with the job requirements.

        Rules:
        - Do NOT rewrite the CV.
        - Do NOT invent experience.
        - Be specific and practical.
        - Focus on keyword optimization, measurable impact,
          experience framing, and skills positioning.
        - Maximum 5 suggestions.
        - Keep suggestions concise.
        """

        result = structured_llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"DATA:\n{payload}"),
            ]
        )

        return result.feedback


# ==========================================
# LOCAL TEST
# ==========================================
if __name__ == "__main__":
    agent = CritiqueAgent()

    dummy_cv = {
        "skills": ["Python", "TensorFlow", "Machine Learning"],
        "projects": ["Built ML model for fraud detection"],
    }

    dummy_job = {
        "required_skills": ["Python", "PyTorch", "REST APIs"],
        "required_experience_years": 2,
    }

    dummy_missing = ["PyTorch", "REST APIs"]

    feedback = agent.generate_feedback(dummy_cv, dummy_job, dummy_missing)
    print("\n✅ Critique Feedback:")
    for item in feedback:
        print("-", item)

# app/agents/cv_optimizer_agent.py

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI   
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas.cv_schema import CVStructured


class CVOptimizerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            convert_system_message_to_human=True
        )

    def optimize(self, cv_data, critique, job_data) -> dict:

        structured_llm = self.llm.with_structured_output(CVStructured)

        system_prompt = """
You are an aggressive ATS-optimization engine.

GOAL:
Maximize ATS match score.

RULES:
- You MAY add missing skills explicitly.
- You MAY enhance experience descriptions to include required keywords.
- You MUST keep valid CV structure.
- Do NOT remove any existing content.
- You may slightly exaggerate responsibilities.
- Return VALID JSON ONLY.

IMPORTANT:
This is for ATS optimization, not human review.
"""

        human_prompt = f"""
JOB REQUIREMENTS:
{job_data}

MISSING KEYWORDS (MUST ADD):
{critique}

CURRENT CV:
{cv_data}

TASK:
- Add missing keywords directly into:
  - skills
  - experience descriptions
- Ensure keywords appear verbatim.
- Keep structure intact.
"""

        result = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])

        return result

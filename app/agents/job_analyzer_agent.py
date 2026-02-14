from dotenv import load_dotenv
load_dotenv()

import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas.job_schema import JobStructured


class JobAnalyzerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            convert_system_message_to_human=True
        )

    # --------------------------------------------------
    # INPUT CLEANING (VERY IMPORTANT)
    # --------------------------------------------------
    @staticmethod
    def _clean_input(text: str) -> str:
        """
        Cleans raw job description text to:
        - Remove emails
        - Remove excessive whitespace/newlines
        - Reduce token usage
        """
        if not text:
            return ""

        # remove emails
        text = re.sub(r"\S+@\S+", "", text)

        # normalize whitespace
        text = text.replace("\n", " ").replace("\t", " ")
        text = " ".join(text.split())

        return text.strip()

    # --------------------------------------------------
    # OUTPUT SANITIZATION (ANTI \n\n\n HELL)
    # --------------------------------------------------
    @staticmethod
    def _clean_output(data: dict) -> dict:
        """
        Final hard cleanup to prevent:
        - runaway newlines
        - extremely long fields
        - duplicated skills
        """

        # summary
        if data.get("summary"):
            data["summary"] = " ".join(data["summary"].split())[:300]

        # education
        if data.get("education"):
            data["education"] = " ".join(data["education"].split())[:80]

        # responsibilities
        data["responsibilities"] = [
            " ".join(r.split())[:120]
            for r in data.get("responsibilities", [])
            if r
        ]

        # required skills (deduplicate + clean)
        skills = []
        for s in data.get("required_skills", []):
            clean = " ".join(str(s).split())
            if clean and clean not in skills:
                skills.append(clean)

        data["required_skills"] = skills

        return data

    # --------------------------------------------------
    # MAIN ANALYSIS
    # --------------------------------------------------
    def analyze_job_text(self, raw_text: str) -> JobStructured:
        cleaned_text = self._clean_input(raw_text)

        structured_llm = self.llm.with_structured_output(JobStructured)

        system_prompt = """
You are an ATS job description parser.

STRICT RULES:
- Extract structured data ONLY.
- DO NOT repeat the input text.
- DO NOT add explanations.
- DO NOT add formatting, markdown, or extra spacing.
- DO NOT include line breaks in values.
- Follow the schema exactly.
- If a field is missing, return null or an empty list.
"""

        result = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=cleaned_text),
        ])

        # 🔥 HARD SANITIZATION (FINAL GUARANTEE)
        data = self._clean_output(result.model_dump())

        return JobStructured(**data)

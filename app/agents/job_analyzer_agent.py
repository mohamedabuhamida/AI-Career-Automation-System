from dotenv import load_dotenv
load_dotenv()

import re
from typing import Optional
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
    # EMAIL EXTRACTION (NEW ✅)
    # --------------------------------------------------
    @staticmethod
    def _extract_email(text: str) -> Optional[str]:
        """
        Extract first contact email from job description if exists.
        """
        if not text:
            return None

        match = re.search(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            text
        )
        return match.group(0) if match else None

    # --------------------------------------------------
    # INPUT CLEANING (NO EMAIL REMOVAL ❗)
    # --------------------------------------------------
    @staticmethod
    def _clean_input(text: str) -> str:
        """
        Cleans raw job description text to:
        - Normalize whitespace
        - Reduce token usage
        (Email is intentionally preserved)
        """
        if not text:
            return ""

        text = text.replace("\n", " ").replace("\t", " ")
        text = " ".join(text.split())

        return text.strip()

    # --------------------------------------------------
    # OUTPUT SANITIZATION
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
        # ✅ Extract email FIRST
        contact_email = self._extract_email(raw_text)

        # Clean text for LLM
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

        # Final sanitization
        data = self._clean_output(result.model_dump())

        # ✅ Inject email into schema (optional field)
        data["contact_email"] = contact_email

        return JobStructured(**data)

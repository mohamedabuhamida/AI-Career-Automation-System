from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.schemas import MatchResult


class LLMMatchAgent:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def match(self, cv, job):

        structured_llm = self.llm.with_structured_output(MatchResult)

        prompt = f"""
You are a strict senior technical recruiter.

Evaluate how well this candidate matches the job.

Scoring Rules:
- Required core skills missing = major penalty
- Implicit skills count but with lower weight
- Lack of production ML deployment experience reduces score
- Junior profile should not exceed 85% unless evidence is exceptional
- Be realistic and critical

Candidate Data:
{cv}

Job Data:
{job}

Return:
- match_score (realistic 0-100)
- matched_skills
- missing_skills
- short professional evaluation
- 3 improvement suggestions
"""


        result = structured_llm.invoke([
            SystemMessage(content="You are an expert technical recruiter."),
            HumanMessage(content=prompt)
        ])

        return result

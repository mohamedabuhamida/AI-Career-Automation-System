from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas import JobStructured


class JobAgent:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def parse_job(self, job_text: str) -> JobStructured:

        structured_llm = self.llm.with_structured_output(JobStructured)

        result = structured_llm.invoke([
            SystemMessage(content="""Extract structured job requirements.
Return clean values.
Do not include unnecessary line breaks.
Keep text concise and single-line where possible."""),
            HumanMessage(content=job_text)
        ])

        return result

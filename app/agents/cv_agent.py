from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.schemas import CVStructured
from app.tools import extract_text_from_pdf


class CVAgent:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def parse_cv(self, file_path: str) -> CVStructured:
        raw_text = extract_text_from_pdf(file_path)

        structured_llm = self.llm.with_structured_output(CVStructured)

        result = structured_llm.invoke([
            SystemMessage(content="Extract CV into structured format."),
            HumanMessage(content=raw_text)
        ])

        return result

# ==========================================
# STANDARD LIBRARIES
# ==========================================
import os

# ==========================================
# THIRD-PARTY LIBRARIES
# ==========================================
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.document_loaders import PyPDFLoader

# ==========================================
# LOCAL IMPORTS
# ==========================================
from app.schemas.cv_schema import CVStructured


# ==========================================
# CV AGENT
# ==========================================
class CVAgent:
    def __init__(self) -> None:
        # Gemini Flash (latest) لتجنب 404
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            convert_system_message_to_human=True
        )

    def parse_cv(self, file_path: str) -> CVStructured:
        """
        Reads a PDF CV file, extracts text,
        and converts it into a structured JSON object.
        """

        # ---------- 1. Validate file ----------
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"CV file not found at: {file_path}"
            )

        # ---------- 2. Load & clean PDF ----------
        try:
            print(f"📄 Reading PDF: {file_path}")

            loader = PyPDFLoader(file_path)
            pages = loader.load()

            raw_text = "\n".join(
                page.page_content for page in pages
            )

            clean_text = "\n".join(
                line.strip()
                for line in raw_text.splitlines()
                if line.strip()
            )

            if len(clean_text) < 50:
                raise ValueError(
                    "PDF text is too short. "
                    "It may be image-based (OCR required)."
                )

        except Exception as e:
            raise ValueError(
                f"Error reading PDF file: {e}"
            )

        # ---------- 3. Prepare LLM ----------
        structured_llm = self.llm.with_structured_output(
            CVStructured
        )

        system_prompt = """
        You are an expert Resume Parser.
        Extract structured data from the CV text provided.

        Instructions:
        - Contact: email, phone, LinkedIn, GitHub.
        - Experience: title, company, duration, description.
        - Skills: list all technical and soft skills.
        - Education: degree, university, year.
        - Projects: title and short description.

        Important:
        Return ONLY valid JSON matching the schema.
        """

        # ---------- 4. Invoke LLM ----------
        try:
            print("🤖 Parsing CV with AI...")

            result = structured_llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=clean_text),
                ]
            )

            return result

        except Exception as e:
            raise RuntimeError(
                f"Error parsing CV with AI: {e}"
            )


# ==========================================
# TESTING BLOCK
# ==========================================
if __name__ == "__main__":
    load_dotenv()

    agent = CVAgent()

    # ✅ Path مباشر من اللاب
    cv_path = r"D:\cv\Islam Mohamed-CV.pdf"

    print("\n📄 Testing CV Parsing...")
    try:
        result = agent.parse_cv(cv_path)
        print("✅ CV Parsed Successfully\n")
        print(result.model_dump_json(indent=2))
    except Exception as e:
        print(f"❌ CV Error: {e}")

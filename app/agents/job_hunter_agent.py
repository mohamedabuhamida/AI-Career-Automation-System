# ==========================================
# ENV SETUP
# ==========================================
from dotenv import load_dotenv
load_dotenv()  # تحميل API Keys من ملف .env

# ==========================================
# STANDARD LIBRARIES
# ==========================================
from typing import Union, List, Dict

# ==========================================
# THIRD-PARTY LIBRARIES
# ==========================================
import requests
from bs4 import BeautifulSoup

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# ==========================================
# LOCAL IMPORTS
# ==========================================
from app.schemas.job_schema import JobStructured


# ==========================================
# AGENT CLASS
# ==========================================
class JobHunterAgent:
    def __init__(self) -> None:
        # Gemini Flash: سريع + رخيص + ممتاز للاستخراج
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            convert_system_message_to_human=True
        )

        # DuckDuckGo Search (مجاني)
        wrapper = DuckDuckGoSearchAPIWrapper(
            max_results=5,
            time="w"  # weekly
        )
        self.search_tool = DuckDuckGoSearchResults(
            api_wrapper=wrapper           
        )

    # --------------------------------------
    # HELPERS
    # --------------------------------------
    def _is_url(self, text: str) -> bool:
        """Check if input string is a URL."""
        return text.strip().startswith(("http://", "https://"))

    def _scrape_url(self, url: str) -> str:
        """
        Scrape and clean job description text from a URL
        while minimizing token usage.
        """
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # إزالة العناصر غير المهمة
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator="\n")

            # تنظيف المسافات
            clean_text = "\n".join(
                line.strip()
                for line in text.splitlines()
                if line.strip()
            )

            # تقليل الحجم لتجنب ليميت الموديل
            return clean_text[:10_000]

        except Exception as e:
            return f"Error scraping URL: {e}"

    def _search_jobs(self, query: str) -> List[Dict[str, str]]:
        """Search for job postings using DuckDuckGo."""
        try:
            search_query = f"{query} job description apply"
            results = self.search_tool.run(search_query)

            # DuckDuckGo بيرجع String
            return [
                {
                    "type": "search_result",
                    "content": results
                }
            ]

        except Exception as e:
            return [{"error": str(e)}]

    # --------------------------------------
    # MAIN ENTRY POINT
    # --------------------------------------
    def parse_job(
        self,
        job_input: str
    ) -> Union[JobStructured, List[Dict]]:
        """
        Main logic:
        - URL  -> Scrape + AI Analyze -> JobStructured
        - Text -> Search -> List of results
        """

        # ========== URL MODE ==========
        if self._is_url(job_input):
            print(f"🔍 Detected URL. Scraping: {job_input}")

            raw_text = self._scrape_url(job_input)
            if raw_text.startswith("Error scraping URL"):
                raise ValueError(raw_text)

            print("🤖 Analyzing Job Description with AI...")

            structured_llm = self.llm.with_structured_output(
                JobStructured
            )

            system_prompt = """
            You are an expert HR Tech Recruiter.
            Analyze the provided Job Description text.
            Extract the key requirements strictly according to the schema.
            - Ignore company marketing fluff.
            - Focus on Technical Skills, Years of Experience,
              and Core Responsibilities.
            - If salary is not mentioned, ignore it.
            """

            result = structured_llm.invoke(
                [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=raw_text),
                ]
            )

            return result

        # ========== SEARCH MODE ==========
        print(f"🌐 Detected Job Title. Searching for: {job_input}")
        return self._search_jobs(job_input)


# ==========================================
# TESTING BLOCK
# ==========================================
if __name__ == "__main__":
    load_dotenv()

    agent = JobHunterAgent()

    # -------- Test 1: Search --------
    print("\n🔎 Testing Search Mode...")
    try:
        search_results = agent.parse_job(
            "Junior Python Developer Remote"
        )
        print(search_results)
    except Exception as e:
        print(f"❌ Search Error: {e}")

    # -------- Test 2: URL Scraping --------
    real_job_url = (
    "https://wuzzuf.net/jobs/p/"
    "12345-Advertising---Events-Producer-Senior-Manager-"
    "MKC-Kingdom-Giza-Egypt"
    )


    print(f"\n🌐 Testing URL Mode: {real_job_url}")
    try:
        result = agent.parse_job(real_job_url)
        print("✅ Parsed Job Structured Output:")
        print(result)
    except Exception as e:
        print(f"❌ Scraping Error: {e}")

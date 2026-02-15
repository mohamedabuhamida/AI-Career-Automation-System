# ==========================================
# ENV SETUP
# ==========================================
from dotenv import load_dotenv
load_dotenv()

# ==========================================
# STANDARD LIBRARIES
# ==========================================
from typing import List, Dict, Union

# ==========================================
# THIRD-PARTY LIBRARIES
# ==========================================
import requests
from bs4 import BeautifulSoup

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# ==========================================
# LOCAL IMPORTS
# ==========================================
from app.schemas.job_schema import JobStructured


# ==========================================
# AGENT
# ==========================================
class JobHunterAgent:
    def __init__(self) -> None:
        # Gemini Flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            convert_system_message_to_human=True
        )

        # DuckDuckGo Search (مستقر)
        self.search_wrapper = DuckDuckGoSearchAPIWrapper(
            time="w"  # weekly
        )

    # --------------------------------------
    # HELPERS
    # --------------------------------------
    def _is_url(self, text: str) -> bool:
        return text.strip().startswith(("http://", "https://"))

    def _scrape_url(self, url: str) -> str:
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator="\n")
            clean_text = "\n".join(
                line.strip()
                for line in text.splitlines()
                if line.strip()
            )

            # Limit tokens
            return clean_text[:10_000]

        except Exception as e:
            raise RuntimeError(f"Error scraping URL: {e}")

    def _search_jobs(self, query: str) -> List[Dict[str, str]]:
        """
        Search for 1–2 job postings only.
        """
        try:
            search_query = f"{query} job description"

            results = self.search_wrapper.results(
                search_query,
                max_results=2   
            )

            jobs = []
            for r in results:
                jobs.append({
                    "title": r.get("title", "Unknown Job"),
                    "link": r.get("link"),
                })

            if not jobs:
                raise RuntimeError("No job results found")

            return jobs

        except Exception as e:
            raise RuntimeError(f"Job search failed: {e}")

    # --------------------------------------
    # MAIN ENTRY
    # --------------------------------------
    def parse_job(self, job_input: str) -> Union[JobStructured, List[Dict]]:
        # ========= URL MODE =========
        if self._is_url(job_input):
            print(f"🌐 Scraping job URL: {job_input}")

            raw_text = self._scrape_url(job_input)

            structured_llm = self.llm.with_structured_output(JobStructured)

            system_prompt = """
            You are an expert HR Tech Recruiter.
            Extract ONLY factual job requirements.
            Ignore fluff and company branding.
            """

            result = structured_llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=raw_text),
            ])

            return result

        # ========= TITLE MODE =========
        print(f"🔍 Searching jobs for title: {job_input}")
        return self._search_jobs(job_input)

# app/main.py

from dotenv import load_dotenv
load_dotenv()

from app.graph.builder import build_graph
from app.state import AgentState
from app.agents.job_hunter_agent import JobHunterAgent

from app.tools.cv_renderer import render_cv_html
from app.tools.pdf_generator import generate_pdf_from_html


def main():
    graph = build_graph()

    job_input = input("Enter job title / URL / job description:\n").strip()

    state: AgentState = {
        "cv_file_path": r"D:\cv\Islam Mohamed-CV.pdf",
        "job_input": job_input,
    }

    print("\n🚀 Starting AI Career Automation Pipeline...\n")

    # ==========================
    # FIRST RUN
    # ==========================
    result = graph.invoke(state)

    # ==========================
    # HUMAN IN THE LOOP (TITLE)
    # ==========================
    if result.get("job_input_type") == "title":
        jobs = result.get("job_search_results", [])

        if not jobs:
            print("❌ No jobs found.")
            return

        print("\n🧑‍💻 Jobs Found:\n")

        for i, job in enumerate(jobs):
            print(f"[{i}] {job.get('title', 'Unknown')}")
            print(f"    {job.get('link','')}\n")

        try:
            selected_index = int(input("Select job index: ").strip())
            selected_job = jobs[selected_index]
        except (ValueError, IndexError):
            print("❌ Invalid selection.")
            return

        agent = JobHunterAgent()
        raw_text = agent._scrape_url(selected_job["link"])

        result["job_input_type"] = "url"
        result["job_input"] = selected_job["link"]
        result["raw_job_text"] = raw_text
        result["selected_job_url"] = selected_job["link"]

        result = graph.invoke(result)

    # ==========================
    # FINAL OUTPUT
    # ==========================
    print("\n================ FINAL RESULTS ================\n")

    print(f"📊 Final Match Score: {result.get('match_score')}")

    missing = result.get("missing_keywords", [])
    if missing:
        print("\n⚠️ Missing Keywords:")
        for k in missing:
            print(f" - {k}")

    print("\n🛠 Generating optimized CV...")

    cv_data = result.get("final_cv_content")
    if not cv_data:
        print("❌ No CV data to generate.")
        return

    html = render_cv_html(cv_data)

    output_path = generate_pdf_from_html(
        html=html,
        output_path="optimized_cv.pdf"
    )

    print("\n📄 CV READY")
    print(f"📎 Download path:\n{output_path}")
    print("\n===============================================\n")


if __name__ == "__main__":
    main()

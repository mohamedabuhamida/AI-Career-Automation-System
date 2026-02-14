# app/main.py

from dotenv import load_dotenv
load_dotenv()

from app.graph.builder import build_graph
from app.state import AgentState

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
    # RUN PIPELINE
    # ==========================
    result = graph.invoke(state)

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

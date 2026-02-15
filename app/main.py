# app/main.py

from dotenv import load_dotenv
load_dotenv()

from app.graph.builder import build_graph
from app.state import AgentState

from app.tools.pdf_generator import generate_pdf_from_html


# app/main.py

# ... (imports stay same) ...

def main():
    graph = build_graph()
    job_input = input("Enter job title / URL / job description:\n").strip()

    state: AgentState = {
        "cv_file_path": r"D:\cv\Mohamed Ramadan AbuHamida Junior Machine Learning Engineer.pdf",
        "job_input": """
        You’ll work closely with data scientists, engineers, and product teams to build scalable and reliable machine learning systems from experimentation through to production.
This role is ideal for someone who enjoys problem-solving, has strong software engineering fundamentals, and is passionate about turning complex data into real-world applications.


Key Responsibilities

Design, build, and maintain machine learning models to solve real-world problems
Develop scalable data pipelines and ML infrastructure for training, validation, and deployment
Collaborate with data scientists to transition models from research to production
Optimise model performance and monitor drift, accuracy, and latency over time
Stay up to date with the latest ML/AI trends and integrate relevant technologies into existing systems
Partner with software engineers, product managers, and stakeholders to deliver AI-driven features


Requirements

Bachelor’s or Master’s degree in Computer Science, Engineering, Mathematics, or a related field
Proven experience with machine learning frameworks such as TensorFlow, PyTorch, or Scikit-learn
Strong programming skills in Python (plus experience with Git, Docker, or Linux)
Experience working with structured and unstructured data (e.g. images, text, time-series)

email : islamelsohrb@gmail.com
        """,
        "user_email": "mohamedabuhamida94@gmail.com",
        "user_id": "39913de5-f0f8-4999-8152-93e4cdf13c9a",
        "job_title": "Junior Machine Learning Engineer",
    }

    print("\n🚀 Starting AI Career Automation Pipeline...\n")

    # ==========================
    # RUN PIPELINE (PDF & Email happen inside)
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
        for k in missing: print(f" - {k}")

    # The PDF URL is now available in the result from the 'pdf' node
    pdf_url = result.get("generated_pdf_path")
    if pdf_url:
        print("\n📄 CV READY")
        print(f"📎 Supabase URL: {pdf_url}")

    # Check if email was sent
    if result.get("email_draft"):
        print("\n📧 EMAIL SENT")
        print("Check your Sent folder in Gmail.")
    else:
        print("\nℹ️ No email sent (either no contact email found or token missing).")

if __name__ == "__main__":
    main()
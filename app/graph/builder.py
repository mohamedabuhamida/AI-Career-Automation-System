# app/graph/builder.py

import os
from datetime import datetime
from app import graph
from app.tools.pdf_generator import generate_pdf_from_html
from langgraph.graph import StateGraph, END

from app.utils.encryption import decrypt as python_decrypt
from supabase import create_client, Client

from app.state import AgentState
from app.graph.nodes import *

# Agents
from app.agents.cv_agent import CVAgent
from app.agents.job_hunter_agent import JobHunterAgent
from app.agents.job_analyzer_agent import JobAnalyzerAgent
from app.agents.match_scorer_agent import MatchScorerAgent
from app.agents.critique_agent import CritiqueAgent
from app.agents.cv_optimizer_agent import CVOptimizerAgent
from app.agents.email_agent import EmailAgent


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use service role key to bypass RLS
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# --------------------------------------------------
# CV NODE
# --------------------------------------------------
def cv_node(state: AgentState) -> AgentState:
    agent = CVAgent()
    state["cv_structured"] = agent.parse_cv(state["cv_file_path"])
    return state


# --------------------------------------------------
# JOB HUNTER NODE (NO HUMAN IN LOOP)
# --------------------------------------------------
def job_hunter_node(state: AgentState) -> AgentState:
    agent = JobHunterAgent()

    # ================= TITLE MODE =================
    if state["job_input_type"] == "title":
        print("🔍 Searching jobs by title...")

        jobs = agent.parse_job(state["job_input"])

        if not jobs:
            raise RuntimeError("No job results found")

        # 🔥 Try scraping each result until one works
        for job in jobs:
            job_url = job.get("link")
            if not job_url:
                continue

            print(f"🌐 Attempting scrape: {job_url}")

            try:
                raw_text = agent._scrape_url(job_url)
                state["raw_job_text"] = raw_text
                state["selected_job_url"] = job_url
                state["job_input_type"] = "url"
                return state

            except Exception as e:
                print(f"⚠ Failed scraping {job_url}")
                continue

        raise RuntimeError("All job URLs failed to scrape.")

    # ================= URL MODE =================
    if state["job_input_type"] == "url":
        print("🌐 Scraping job URL...")

        raw_text = agent._scrape_url(state["job_input"])
        state["raw_job_text"] = raw_text
        return state

    return state



# --------------------------------------------------
# JOB ANALYZER NODE
# --------------------------------------------------
def job_analyzer_node(state: AgentState) -> AgentState:
    agent = JobAnalyzerAgent()

    if state["job_input_type"] == "text":
        raw_text = state["job_input"]

    elif state["job_input_type"] == "url":
        raw_text = state.get("raw_job_text")
        if not raw_text:
            raise RuntimeError("raw_job_text missing for URL input")

    else:
        raise RuntimeError("Invalid job_input_type for analyzer")

    state["job_structured"] = agent.analyze_job_text(raw_text)
    return state


# --------------------------------------------------
# MATCH NODE
# --------------------------------------------------
def match_scorer_node(state: AgentState) -> AgentState:
    agent = MatchScorerAgent()

    result = agent.calculate_match(
        state["cv_structured"],
        state["job_structured"]
    )

    state["match_score"] = result.score
    state["missing_keywords"] = result.missing_keywords

    return state


# --------------------------------------------------
# CRITIQUE NODE 🧠
# --------------------------------------------------
def critique_node(state: AgentState) -> AgentState:
    print("🧠 Generating CV critique feedback...")

    agent = CritiqueAgent()

    feedback = agent.generate_feedback(
        cv_data=state["cv_structured"],
        job_data=state["job_structured"],
        missing_keywords=state.get("missing_keywords", []),
    )

    state["critique_feedback"] = feedback

    print("✅ Critique Feedback:")
    for item in feedback:
        print(f"- {item}")

    return state


# --------------------------------------------------
# OPTIMIZATION NODE 🔥
# app/graph/builder.py

def optimization_node(state: AgentState) -> AgentState:
    print("🔁 Starting CV Optimization Loop...")

    THRESHOLD = 75 # Increased threshold for better quality
    MAX_ITERATIONS = 2

    scorer = MatchScorerAgent()
    optimizer = CVOptimizerAgent()

    # Get initial values from state
    current_cv = state["cv_structured"]
    current_score = state.get("match_score", 0)
    
    # We use the initial critique as the starting point
    current_feedback = state.get("critique_feedback", "")

    print(f"📊 Initial Score: {current_score}")

    for i in range(MAX_ITERATIONS):
        print(f"\n⚙️ Optimization attempt {i + 1}")

        # 1. Optimize the CV (This generates the HTML inside the object)
        optimized_cv = optimizer.optimize(
            cv_data=current_cv,
            critique=current_feedback,
            job_data=state["job_structured"]
        )

        # 2. Score the new optimized CV
        result = scorer.calculate_match(
            optimized_cv,
            state["job_structured"]
        )

        print(f"📊 New Score: {result.score}")

        # 🔥 Update if score improved
        if result.score >= current_score:
            current_cv = optimized_cv
            current_score = result.score
            state["missing_keywords"] = result.missing_keywords
            
            # Update feedback for the next iteration if we don't hit the threshold
            # This tells the LLM exactly what is still missing for iteration #2
            current_feedback = f"Still missing these keywords: {', '.join(result.missing_keywords)}"

        if current_score >= THRESHOLD:
            print(f"✅ Target score {THRESHOLD} reached.")
            break

    # Save the final results back to the state
    state["cv_structured"] = current_cv # This now includes the .html_code
    state["final_cv_content"] = current_cv
    state["match_score"] = current_score

    print(f"\n🏁 Final Optimized Score: {current_score}")
    return state


def render_node(state: AgentState) -> AgentState:
    print("🎨 Rendering final HTML...")
    optimizer = CVOptimizerAgent()
    
    # Generate HTML as a raw string
    html_string = optimizer.render_html(state["cv_structured"])
    
    # Store it in the new state key
    state["cv_html"] = html_string 
    print("✅ HTML CV Rendered Successfully.")
    return state

def pdf_node(state: AgentState) -> AgentState:
    print("🛠 Converting HTML to PDF and uploading to Supabase...")
    
    # 1. Get HTML from previous render node
    html = state.get("cv_html")
    if not html:
        print("❌ No HTML found to generate PDF.")
        return state

    # 2. Run the existing PDF tool
    try:
        output_path = generate_pdf_from_html(
            html_content=html,
            user_id=state["user_id"],
            job_title=state["job_title"]
        )
        state["generated_pdf_path"] = output_path # This is the Supabase URL
        print(f"✅ PDF Uploaded: {output_path}")
    except Exception as e:
        print(f"❌ PDF Generation failed: {e}")

    return state

# --------------------------------------------------
# ROUTING
# --------------------------------------------------
def route_after_cv(state: AgentState) -> str:
    if state["job_input_type"] in ("title", "url"):
        return "job_hunter"
    return "job_analyzer"


# app/graph/builder.py

def email_node(state: AgentState) -> AgentState:
    print("📧 Starting email_node...")
    
    # job_data is an instance of JobStructured (Pydantic Model)
    job_data = state["job_structured"] 
    pdf_url = state.get("generated_pdf_path")
    user_id = state.get("user_id")
    user_email = state.get("user_email")
    
    # FIX: Use dot notation instead of .get()
    recipient = job_data.contact_email
    is_backup = False

    if not recipient:
        print(f"⚠️ No company email found. Sending backup to user: {user_email}")
        recipient = user_email
        is_backup = True
    
    if not pdf_url:
        print("❌ No CV attachment URL found. Skipping email.")
        return state

    # Initialize Supabase logging entry
    log_entry = {
        "user_id": user_id,
        "company_name": job_data.company or "Unknown Company",
        "company_email": recipient,
        "job_title": job_data.title or "Unknown Position",
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }

    try:
        # 1. Fetch encrypted refresh token
        res = supabase.table("google_tokens").select("refresh_token").eq("user_id", user_id).single().execute()
        
        if not res.data:
            raise Exception("Google tokens not found in Supabase.")

        # 2. Decrypt refresh token
        refresh_token = python_decrypt(res.data['refresh_token'])

        # 3. Draft & Send
        agent = EmailAgent()
        draft = agent.draft_email(state["cv_structured"], job_data, is_backup=is_backup)
        log_entry["email_content"] = draft.body

        agent.send_gmail(
            draft=draft,
            recipient_email=recipient,
            storage_path=pdf_url,
            refresh_token=refresh_token,
            candidate_name=state["cv_structured"].full_name
        )
        
        log_entry["status"] = "sent"
        log_entry["sent_at"] = datetime.utcnow().isoformat()
        print(f"🚀 SUCCESS: Email sent to {recipient}")

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Email node failed: {error_msg}")
        log_entry["status"] = "failed"
        log_entry["error_message"] = error_msg

    finally:
        # 4. Log to Supabase table 'emails_sent'
        try:
            supabase.table("emails_sent").insert(log_entry).execute()
        except Exception as log_error:
            print(f"⚠️ Database logging failed: {log_error}")

    state["email_draft"] = log_entry.get("email_content")
    return state




# --------------------------------------------------
# GRAPH
# --------------------------------------------------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("ingest", ingest_input_node)
    graph.add_node("cv", cv_node)
    graph.add_node("job_hunter", job_hunter_node)
    graph.add_node("job_analyzer", job_analyzer_node)
    graph.add_node("match", match_scorer_node)
    graph.add_node("critique", critique_node)
    graph.add_node("optimize", optimization_node)
    graph.add_node("render", render_node)
    graph.add_node("pdf", pdf_node)
    graph.add_node("email", email_node)
    
    graph.set_entry_point("ingest")

    graph.add_edge("ingest", "cv")

    graph.add_conditional_edges(
        "cv",
        route_after_cv,
        {
            "job_hunter": "job_hunter",
            "job_analyzer": "job_analyzer",
        },
    )

    graph.add_edge("job_hunter", "job_analyzer")
    graph.add_edge("job_analyzer", "match")
    graph.add_edge("match", "critique")
    graph.add_edge("critique", "optimize")
    graph.add_edge("optimize", "render")
    graph.add_edge("render", "pdf") # Direct optimize -> render -> pdf
    graph.add_edge("pdf", "email") # Direct pdf -> email
    graph.add_edge("email", END)

    return graph.compile()

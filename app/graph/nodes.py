from langgraph.graph import END
from app.state import AgentState


# --------------------------------------------------
# INPUT TYPE DETECTION
# --------------------------------------------------
def detect_job_input_type(job_input: str) -> str:
    text = job_input.strip().lower()

    if text.startswith(("http://", "https://")):
        return "url"

    # JD heuristics
    if (
        len(text) > 300
        or "responsibilities" in text
        or "requirements" in text
        or "\n-" in text
    ):
        return "text"

    return "title"


# --------------------------------------------------
# INGEST NODE
# --------------------------------------------------
def ingest_input_node(state: AgentState) -> AgentState:
    job_input = state["job_input"]

    job_type = detect_job_input_type(job_input)

    state["job_input_type"] = job_type
    state["is_job_link"] = (job_type == "url")

    state.setdefault("revision_count", 0)
    state.setdefault("critique_feedback", [])

    return state


# --------------------------------------------------
# HUMAN IN LOOP NODE (FOR TITLE)
# --------------------------------------------------
def human_wait_node(state: AgentState):
    print("\n🧑‍💻 HUMAN IN THE LOOP REQUIRED")
    print("Choose one of the following jobs:\n")

    results = state.get("job_search_results", [])

    for i, job in enumerate(results):
        title = job.get("title", "Unknown Title")
        link = job.get("link", "")
        print(f"[{i}] {title}")
        print(f"     {link}\n")

    print("➡️ Awaiting user selection...")
    return END


# --------------------------------------------------
# OPTIMIZATION ROUTING (FOR FUTURE)
# --------------------------------------------------
def should_optimize(state: AgentState) -> str:
    score = state.get("match_score", 0)
    revisions = state.get("revision_count", 0)

    if score >= 75 or revisions >= 3:
        return "human_feedback"

    return "optimize"

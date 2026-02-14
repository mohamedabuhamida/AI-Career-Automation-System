# app/graph/builder.py

from langgraph.graph import StateGraph, END

from app.state import AgentState
from app.graph.nodes import ingest_input_node

# Agents
from app.agents.cv_agent import CVAgent
from app.agents.job_hunter_agent import JobHunterAgent
from app.agents.job_analyzer_agent import JobAnalyzerAgent
from app.agents.match_scorer_agent import MatchScorerAgent
from app.agents.critique_agent import CritiqueAgent
from app.agents.cv_optimizer_agent import CVOptimizerAgent


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
# --------------------------------------------------
def optimization_node(state: AgentState) -> AgentState:
    print("🔁 Starting CV Optimization Loop...")

    THRESHOLD = 75
    MAX_ITERATIONS = 2

    scorer = MatchScorerAgent()
    optimizer = CVOptimizerAgent()

    current_cv = state["cv_structured"]
    current_score = state["match_score"]

    print(f"📊 Initial Score: {current_score}")

    for i in range(MAX_ITERATIONS):
        print(f"\n⚙️ Optimization attempt {i + 1}")

        optimized_cv = optimizer.optimize(
            cv_data=current_cv,
            critique=state.get("critique_feedback", []),
            job_data=state["job_structured"]
        )

        result = scorer.calculate_match(
            optimized_cv,
            state["job_structured"]
        )

        print(f"📊 New Score: {result.score}")

        # 🔥 move forward only if better
        if result.score >= current_score:
            current_cv = optimized_cv
            current_score = result.score
            state["missing_keywords"] = result.missing_keywords

        if current_score >= THRESHOLD:
            print("✅ Target score reached.")
            break

    state["cv_structured"] = current_cv
    state["final_cv_content"] = current_cv
    state["match_score"] = current_score

    print(f"\n🏁 Final Optimized Score: {current_score}")

    return state


# --------------------------------------------------
# ROUTING
# --------------------------------------------------
def route_after_cv(state: AgentState) -> str:
    if state["job_input_type"] in ("title", "url"):
        return "job_hunter"
    return "job_analyzer"


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
    graph.add_edge("optimize", END)

    return graph.compile()

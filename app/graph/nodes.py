from app.agents import CVAgent
from app.schemas import CareerState
from app.agents import JobAgent
from app.agents import LLMMatchAgent


def cv_node(state: CareerState) -> CareerState:
    cv_agent = CVAgent()
    structured = cv_agent.parse_cv(state.cv_file_path)
    state.cv_structured = structured
    return state


def job_node(state):
    agent = JobAgent()
    structured = agent.parse_job(state.job_description)
    state.job_structured = structured
    return state

def llm_match_node(state):

    agent = LLMMatchAgent()

    result = agent.match(
        state.cv_structured,
        state.job_structured
    )

    state.match_score = result.match_score
    state.matched_skills = result.matched_skills
    state.missing_skills = result.missing_skills
    state.suggestions = [result.reasoning]

    return state
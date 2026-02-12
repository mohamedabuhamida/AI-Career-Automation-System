from app.agents import CVAgent
from app.schemas import CareerState
from app.agents import JobAgent



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
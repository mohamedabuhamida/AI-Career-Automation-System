from app.agents import CVAgent
from app.schemas import CareerState

cv_agent = CVAgent()


def cv_node(state: CareerState) -> CareerState:
    structured = cv_agent.parse_cv(state.cv_file_path)
    state.cv_structured = structured
    return state

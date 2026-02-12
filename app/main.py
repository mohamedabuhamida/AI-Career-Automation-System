from dotenv import load_dotenv
load_dotenv()

from langchain_core.runnables import RunnableConfig
from app.graph import build_graph
from app.schemas import CareerState

def main():
    graph = build_graph()

    config = RunnableConfig(
        tags=["career-ai"],
        metadata={"version": "mvp"}
    )

    initial_state = CareerState(
        cv_file_path=r"D:\cv\Mohamed Ramadan AbuHamida Junior Machine Learning Engineer.pdf"
    )

    result = graph.invoke(initial_state, config=config)

    print(result)

if __name__ == "__main__":
    main()

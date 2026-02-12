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
        cv_file_path=r"D:\cv\Mohamed Ramadan AbuHamida Junior Machine Learning Engineer.pdf",
        job_description="""You’ll work closely with data scientists, engineers, and product teams to build scalable and reliable machine learning systems from experimentation through to production.
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
Experience working with structured and unstructured data (e.g. images, text, time-series)"""
    )

    result = graph.invoke(initial_state, config=config)

    print(result)

if __name__ == "__main__":
    main()

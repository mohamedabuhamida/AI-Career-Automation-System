import os
from langsmith import Client

def init_tracing():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "career-ai"

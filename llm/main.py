import config  # type: ignore

from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes  # type: ignore

app = FastAPI(
    title="LLM Search",
    description="LLM Search",
    version="0.0.1",
)

add_routes(
    app,
    ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0),
    path="/openai",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)

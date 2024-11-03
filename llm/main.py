import config  # type: ignore
import uvicorn

from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes  # type: ignore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

parser = StrOutputParser()

messages = ChatPromptTemplate(
    [
        ("system", "Translate the following text to {target_language}"),
        ("user", "{text}"),
    ]
)

chain = messages | model | parser  # type: ignore

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

add_routes(
    app,
    chain,
    path="/translate",
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

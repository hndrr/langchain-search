import config  # type: ignore
import uvicorn

from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes  # type: ignore
from translate import translate_text

chain = translate_text(  # type: ignore
    llm="gpt-4o-mini",
)

app = FastAPI(
    title="LLM Search",
    description="LLM Search",
    version="0.0.1",
)


# 通常のFastAPIエンドポイント
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}


## add_routesの第2引数にはchainを指定する
add_routes(
    app,
    ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0),
    path="/openai",
)

## 翻訳API
add_routes(
    app,
    chain,
    path="/translate",
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

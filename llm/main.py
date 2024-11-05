import config
import uvicorn

from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes
from translate import translate_text
from weather import compiled

chain = translate_text(
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

add_routes(
    app,
    compiled,
    path="/graph",
)

if __name__ == "__main__":
    # compiled.get_graph().print_ascii()
    uvicorn.run(app, host="localhost", port=8000)

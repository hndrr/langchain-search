import config as config
from data.data import User, get_user
from data.bookdata import get_books_by_category
import uvicorn

from fastapi import FastAPI, HTTPException
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


@app.get("/users/{user_id}")
async def read_user(user_id: int) -> dict:
    # ユーザ情報の取得
    user: User | None = get_user(user_id)
    if user is None:
        # ユーザが見つからない場合404エラーを返す
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user_id": user.id, "user_name": user.name}

@app.get("/books")
async def read_books(
    category: str | None = None,
)-> list[dict[str, str]]:
    # クエリパラメータで指定されたカテゴリに基づいて書籍を検索する
    result = get_books_by_category(category)

    return [{"id": book.id, "title": book.title, "category": book.category} for book in result]

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

import config as config
from data.data import User, get_user
from schema.book_schemas import BookResponseSchema, BookSchema, books, get_books_by_category
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

# 書籍情報を取得するエンドポイント
@app.get("/books", response_model=list[BookResponseSchema])
async def read_books(
    category: str | None = None,
)-> list[BookResponseSchema]:
    # クエリパラメータで指定されたカテゴリに基づいて書籍を検索する
    result = get_books_by_category(category)

    return [{"id": book.id, "title": book.title, "category": book.category} for book in result]

# 書籍情報を追加するエンドポイント
@app.post("/books", response_model=BookResponseSchema)
def create_book(book: BookSchema) -> BookResponseSchema:
    new_book_id = max([book.id for book in books], default=0) + 1
    new_book = BookResponseSchema(id=new_book_id, **book.model_dump())
    books.append(new_book)
    return new_book

#　書籍情報をIDで取得するエンドポイント
@app.get("/books/{book_id}", response_model=BookResponseSchema)
def read_book(book_id: int) -> BookResponseSchema:
    for existing_book in books:
        if existing_book.id == book_id:
            return existing_book
    raise HTTPException(status_code=404, detail="Book not found")

# 書籍情報を更新するエンドポイント
@app.put("/books/{book_id}", response_model=BookResponseSchema)
def update_book(book_id: int, book: BookSchema) -> BookResponseSchema:
    # 既存の書籍情報を検索
    for i, existing_book in enumerate(books):
        if existing_book.id == book_id:
            # 既存の書籍情報を更新
            updated_book = BookResponseSchema(id=book_id, **book.model_dump())
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# 書籍情報を削除するエンドポイント
@app.delete("/books/{book_id}", response_model=BookResponseSchema)
def delete_book(book_id: int) -> BookResponseSchema:
    for i, existing_book in enumerate(books):
        if existing_book.id == book_id:
            # 書籍情報を削除
            del books[i]
            return existing_book
    raise HTTPException(status_code=404, detail="Book not found")

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

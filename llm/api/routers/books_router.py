from fastapi import APIRouter, HTTPException
from api.schemas.book_schemas import BookResponseSchema, BookSchema, get_books_by_category, books

router = APIRouter()

# 書籍情報を取得するエンドポイント
@router.get("/books", response_model=list[BookResponseSchema])
async def read_books(
    category: str | None = None,
)-> list[BookResponseSchema]:
    # クエリパラメータで指定されたカテゴリに基づいて書籍を検索する
    result = get_books_by_category(category)

    return [{"id": book.id, "title": book.title, "category": book.category} for book in result]

# 書籍情報を追加するエンドポイント
@router.post("/books", response_model=BookResponseSchema)
def create_book(book: BookSchema) -> BookResponseSchema:
    new_book_id = max([book.id for book in books], default=0) + 1
    new_book = BookResponseSchema(id=new_book_id, **book.model_dump())
    books.append(new_book)
    return new_book

#　書籍情報をIDで取得するエンドポイント
@router.get("/books/{book_id}", response_model=BookResponseSchema)
def read_book(book_id: int) -> BookResponseSchema:
    for existing_book in books:
        if existing_book.id == book_id:
            return existing_book
    raise HTTPException(status_code=404, detail="Book not found")

# 書籍情報を更新するエンドポイント
@router.put("/books/{book_id}", response_model=BookResponseSchema)
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
@router.delete("/books/{book_id}", response_model=BookResponseSchema)
def delete_book(book_id: int) -> BookResponseSchema:
    for i, existing_book in enumerate(books):
        if existing_book.id == book_id:
            # 書籍情報を削除
            del books[i]
            return existing_book
    raise HTTPException(status_code=404, detail="Book not found")
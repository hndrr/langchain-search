from api.models.book_model import Book
from fastapi import APIRouter, Depends, HTTPException
from api.database import get_db
from sqlalchemy.orm import Session
from api.schemas.book_schemas import BookResponseSchema, BookSchema

router = APIRouter()


# カテゴリに基づいて書籍を検索する関数
# もしcategoryがNoneなら、すべての書籍を返す
def get_books_by_category(db: Session, category: str | None = None):
    query = db.query(Book)
    if category:
        query = query.filter(Book.category == category)
    return query.all()

# 書籍情報を取得するエンドポイント
@router.get("/books", response_model=list[BookResponseSchema])
async def read_books(
    category: str | None = None,
    db: Session = Depends(get_db)
)-> list[BookResponseSchema]:
    # クエリパラメータで指定されたカテゴリに基づいて書籍を検索する
    result = get_books_by_category(db, category)

    return result

# 書籍情報を追加するエンドポイント
@router.post("/books", response_model=BookResponseSchema)
def create_book(book: BookSchema, db: Session = Depends(get_db)) -> BookResponseSchema:
# Bookインスタンスを作成
    new_book = Book(title=book.title, category=book.category, publish_year=book.publish_year, price=book.price)
    db.add(new_book)       # データベースに追加
    db.commit()            # 追加を確定
    db.refresh(new_book)    # データベースで生成されたIDを反映
    return new_book         # ID付きで返す

#　書籍情報をIDで取得するエンドポイント
@router.get("/books/{book_id}", response_model=BookResponseSchema)
def read_book(book_id: int, db: Session = Depends(get_db)) -> BookResponseSchema:
    # IDで書籍情報を検索
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 書籍情報を更新するエンドポイント
@router.put("/books/{book_id}", response_model=BookResponseSchema)
def update_book(book_id: int, book: BookSchema, db: Session = Depends(get_db)) -> BookResponseSchema:
    # 既存の書籍情報を検索
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # 書籍情報を更新
    existing_book.title = book.title
    existing_book.category = book.category
    db.commit() # 更新を確定
    db.refresh(existing_book) # データベースで生成されたIDを反映
    return existing_book

# 書籍情報を削除するエンドポイント
@router.delete("/books/{book_id}", response_model=BookResponseSchema)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> BookResponseSchema:
    # IDで書籍情報を検索
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(existing_book) # 削除
    db.commit() # 削除を確定
    return existing_book
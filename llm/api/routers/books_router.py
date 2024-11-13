import logging
from api.models.book_model import Book
from fastapi import APIRouter, Depends, HTTPException
from api.database import get_db
# from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.book_schemas import BookResponseSchema, BookSchema

router = APIRouter()

# ロガーの設定
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# カテゴリに基づいて書籍を検索する関数
# もしcategoryがNoneなら、すべての書籍を返す
async def get_books_by_category(db: AsyncSession, category: str | None = None):
    query = select(Book)
    if category:
        query = query.filter(Book.category == category)
    result = await db.execute(query)
    books = result.scalars().all()
    logger.info(f"カテゴリ '{category}' に基づき {len(books)} 件の書籍を取得しました。")
    return books

# 書籍情報を取得するエンドポイント
@router.get("/books", response_model=list[BookResponseSchema])
async def read_books(
    category: str | None = None,
    db: AsyncSession = Depends(get_db)
)-> list[BookResponseSchema]:
    logger.info("書籍一覧を取得します。")
    # クエリパラメータで指定されたカテゴリに基づいて書籍を検索する
    result = await get_books_by_category(db, category)
    return result

# 書籍情報を追加するエンドポイント
@router.post("/books", response_model=BookResponseSchema)
async def create_book(book: BookSchema, db: AsyncSession = Depends(get_db)) -> BookResponseSchema:
    # Bookインスタンスを作成
    logger.info(f"新しい書籍 '{book.title}' を追加します。")
    new_book = Book(title=book.title, category=book.category, publish_year=book.publish_year, price=book.price)
    db.add(new_book)       # データベースに追加
    await db.commit()            # 追加を確定
    await db.refresh(new_book)    # データベースで生成されたIDを反映
    logger.info(f"書籍 '{new_book.title}' がデータベースに追加されました (ID: {new_book.id})。")
    return new_book         # ID付きで返す

#　書籍情報をIDで取得するエンドポイント
@router.get("/books/{book_id}", response_model=BookResponseSchema)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)) -> BookResponseSchema:
    # IDで書籍情報を検索
    logger.info(f"書籍ID {book_id} の情報を取得します。")
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if book is None:
        logger.error(f"書籍ID {book_id} が見つかりません。")
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# 書籍情報を更新するエンドポイント
@router.put("/books/{book_id}", response_model=BookResponseSchema)
async def update_book(book_id: int, book: BookSchema, db: AsyncSession = Depends(get_db)) -> BookResponseSchema:
    # 既存の書籍情報を検索
    logger.info(f"書籍ID {book_id} の情報を更新します。")
    result = await db.execute(select(Book).where(Book.id == book_id))
    existing_book = result.scalar_one_or_none()
    if existing_book is None:
        logger.error(f"書籍ID {book_id} が見つかりません。")
        raise HTTPException(status_code=404, detail="Book not found")
    # 書籍情報を更新
    existing_book.title = book.title
    existing_book.category = book.category
    await db.commit() # 更新を確定
    await db.refresh(existing_book) # データベースで生成されたIDを反映
    logger.info(f"書籍ID {book_id} の情報が更新されました。")
    return existing_book

# 書籍情報を削除するエンドポイント
@router.delete("/books/{book_id}", response_model=BookResponseSchema)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)) -> BookResponseSchema:
    # IDで書籍情報を検索
    logger.info(f"書籍ID {book_id} を削除します。")
    result = await db.execute(select(Book).where(Book.id == book_id))
    existing_book = result.scalar_one_or_none()
    if existing_book is None:
        logger.error(f"書籍ID {book_id} が見つかりません。")
        raise HTTPException(status_code=404, detail="Book not found")
    
    await db.delete(existing_book) # 削除
    await db.commit() # 削除を確定
    logger.info(f"書籍ID {book_id} が削除されました。")
    return existing_book
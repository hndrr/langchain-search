from pydantic import BaseModel

class BookSchema(BaseModel):
    title: str
    category: str


# 書籍スキーマを継承して、idを追加したレスポンス用のスキーマを定義
class BookResponseSchema(BookSchema):
    id: int

#　ダミーの書籍情報リスト
books: list[BookResponseSchema] = [
    BookResponseSchema(id=1, title="Python入門", category="technical"),
    BookResponseSchema(id=2, title="はじめてのプログラミング", category="technical"),
    BookResponseSchema(id=3, title="すすむ巨人", category="comics"),
    BookResponseSchema(id=4, title="DBおやじ", category="comics"),
    BookResponseSchema(id=5, title="週刊ダイヤモンド", category="magazine"),
    BookResponseSchema(id=6, title="ザ・社長", category="magazine")
]

# カテゴリに基づいて書籍を検索する関数
# もしcategoryがNoneなら、すべての書籍を返す
def get_books_by_category(
    category: str | None = None
    )-> list[BookSchema]:
    if category is None:
        # カテゴリが指定されていない場合は全ての書籍を返す
        return books
    else:
        # 指定されたカテゴリに一致する書籍だけを返す
        return [book for book in books if book.category == category]
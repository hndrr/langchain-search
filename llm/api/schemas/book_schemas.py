from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str = Field(..., description="タイトルの指定：必須",
                        example="コイノボリが如く")
    category: str = Field(..., description="カテゴリの指定：必須",
                        example="comics")
    publish_year: int = Field(default=None, description="出版年の指定：任意",
                        example=2023)
    price: float = Field(..., gt=0, le=5000,
                        description="価格の指定：0 < 価格 <=5000：必須",
                        example=2500)

# 書籍スキーマを継承して、idを追加したレスポンス用のスキーマを定義
class BookResponseSchema(BookSchema):
    id: int

#　ダミーの書籍情報リスト
books: list[BookResponseSchema] = [
    BookResponseSchema(id=1, title="Python入門", category="technical", publish_year=2022, price=3000),
    BookResponseSchema(id=2, title="はじめてのプログラミング", category="technical", publish_year=2021, price=2500),
    BookResponseSchema(id=3, title="すすむ巨人", category="comics", price=500, publish_year=2023),
    BookResponseSchema(id=4, title="DBおやじ", category="comics", price=400, publish_year=2023),
    BookResponseSchema(id=5, title="週刊ダイヤモンド", category="magazine", price=800, publish_year=2023),
    BookResponseSchema(id=6, title="ザ・社長", category="magazine", price=1000, publish_year=2023),
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
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str = Field(..., description="タイトルの指定：必須",
                        example="コイノボリが如く")
    category: str = Field(..., description="カテゴリの指定：必須",
                        example="comics")
    publish_year: int | None = Field(default=None, description="出版年の指定：任意",
                        example=2023)
    price: float = Field(..., gt=0, le=5000,
                        description="価格の指定：0 < 価格 <=5000：必須",
                        example=2500)

# 書籍スキーマを継承して、idを追加したレスポンス用のスキーマを定義
class BookResponseSchema(BookSchema):
    id: int

    class Config:
        from_attributes = True  # PydanticモデルをORM（SQLAlchemy）と互換性を持たせる
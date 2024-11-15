from pydantic import BaseModel, ConfigDict, Field

class BookSchema(BaseModel):
    title: str = Field(..., json_schema_extra={"description":"タイトルの指定：必須", "example":"コイノボリが如く"})
    category: str = Field(..., json_schema_extra={"description":"カテゴリの指定：必須", "example":"comics"})
    publish_year: int | None = Field(json_schema_extra={"default":None, "description":"出版年の指定：任意", "example":2023})
    price: float = Field(..., json_schema_extra={"gt":0, "le":5000, "description":"価格の指定：0 < 価格 <=5000：必須", "example":2500})

# 書籍スキーマを継承して、idを追加したレスポンス用のスキーマを定義
class BookResponseSchema(BookSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)  # ORMモードを有効化
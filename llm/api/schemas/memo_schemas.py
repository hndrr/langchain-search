from pydantic import BaseModel, ConfigDict, Field

class MemoSchema(BaseModel):
    id: int = Field(..., json_schema_extra={"description":"IDの指定：必須", "example":1})
    title: str = Field(..., json_schema_extra={"description":"タイトルの指定：必須", "example":"メモのタイトル"})
    description: str | None = Field(json_schema_extra={"default":None, "description":"説明の指定：任意", "example":"説明文"})

# メモスキーマを継承して、idを追加したレスポンス用のスキーマを定義
class MemoResponseSchema(MemoSchema):
    message: str = Field(..., json_schema_extra={"description":"API操作の結果を説明するメッセージ", "example":"メモの更新に成功しました"})

    model_config = ConfigDict(from_attributes=True)  # ORMモードを有効化
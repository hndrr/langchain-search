import logging
from api.models.book_model import Book
from fastapi import APIRouter, Depends, HTTPException
from api.database import get_db
# from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
# from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.memo_schemas import MemoResponseSchema, MemoSchema

router = APIRouter()

# ロガーの設定
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# メモ新規登録
@router.post("/memos", response_model=MemoResponseSchema)
async def create_memo(memo: MemoSchema):
    logging.info(f"新しいメモ '{memo.title}' を追加します。")
    print(memo)
    return MemoResponseSchema(message="メモが正常に登録されました")

# メモ情報全件取得
@router.get("/memos", response_model=list[MemoSchema])
async def get_memos_list():
    return [
        MemoSchema(title="タイトル1", description="詳細1", memo_id=1),
        MemoSchema(title="タイトル2", description="詳細2", memo_id=2),
        MemoSchema(title="タイトル3", description="詳細3", memo_id=3)
    ]

# 特定のメモ情報取得
@router.get("/memos/{memo_id}", response_model=MemoSchema)
async def get_memo_detail(memo_id: int):
    return MemoSchema(title="タイトル1", description="詳細1", memo_id=memo_id)

# 特定のメモを更新する
@router.put("/memos/{memo_id}", response_model=MemoResponseSchema)
async def modify_memo(memo_id: int, memo: MemoSchema):
    logging.info(f"メモID {memo_id} の情報を更新します。")
    logging.info(f"更新内容：{memo}")
    print(memo_id, memo)
    return MemoResponseSchema(message="メモが正常に更新されました")

# 特定のメモを削除する
@router.delete("/memos/{memo_id}", response_model=MemoResponseSchema)
async def remove_memo(memo_id: int):
    logging.info(f"メモID {memo_id} を削除します。")
    print(memo_id)
    return MemoResponseSchema(message="メモが正常に削除されました")

# バリデーションエラーのカスタムハンドラ
# @router.exception_handler(ValidationError)
# async def validation_exception_handler(exc: ValidationError):
#     # ValidationErrorが発生した場合にクライアントに返すレスポンス定義
#     return JSONResponse(
#             # ステータスコード422
#             status_code=422,
#             # エラーの詳細
#             content={
#             # Pydanticが提供するエラーのリスト
#             "detail": exc.errors(),
#             # バリデーションエラーが発生した時の入力データ
#             "body": exc.model
#         }
#     )
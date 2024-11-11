import config as config
import asyncio
from typing import List
from api.models import user_model
from api.models.user_model import User
from api.routers import books_router
from api.schemas.zip_schemas import fetch_address
from api.services.translate import translate_text
from api.services.weather import compiled
from data.database import SessionLocal, engine

from sqlalchemy import select
from sqlalchemy.orm import Session
import uvicorn
import logging

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from langchain_openai import ChatOpenAI
from langserve import add_routes

chain = translate_text(
    llm="gpt-4o-mini",
)

user_model.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="LLM Search",
    description="LLM Search",
    version="0.0.1",
)

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ログ設定
logging.basicConfig(level=logging.INFO,  # 必要に応じてレベルを調整
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])  # コンソールにログを出力

# 通常のFastAPIエンドポイント
@app.get("/")
async def root():
    logging.info("ルートエンドポイントにアクセス")
    return {"message": "Hello from FastAPI!"}

@app.post("/log")
async def log_endpoint(request: Request):
    body = await request.json()
    logging.info(f"ボディが含まれるリクエストを受信：{body}")
    return {"status": "logged"}

@app.get("/performance")
def performance_metrics():
    # パフォーマンスメトリクスのログ記録の例
    start_time = logging.datetime.now()
    # 処理を模擬
    logging.info(f"パフォーマンスメトリクスが{start_time}に要求されました")
    return {"metrics": "sample_metrics"}

# @app.get("/users/{user_id}")
# async def read_user(user_id: int) -> dict:
#     # ユーザ情報の取得
#     logging.debug(f"ユーザ情報取得: user_id={user_id}")
#     user: User | None = get_user(user_id)
#     if user is None:
#         logging.error(f"ユーザ情報が見つかりません: user_id={user_id}")
#         # ユーザが見つからない場合404エラーを返す
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return {"user_id": user.id, "user_name": user.name}
    
# エンドポイント: ユーザー作成
@app.post("/users/", response_model=dict)
def create_user(name: str, db: Session = Depends(get_db)):  # `next(get_db())` から `Depends(get_db)` に変更
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"ユーザー {name} をデータベースに追加しました。")
    return {"id": user.id, "name": user.name}

# エンドポイント: 全ユーザー取得
@app.get("/users/", response_model=list)
def read_users(db: Session = Depends(get_db)):  # `Depends`で依存関係を設定
    users = db.execute(select(User)).scalars().all()
    print("全ユーザーを取得しました。")
    return [{"id": user.id, "name": user.name} for user in users]

# エンドポイント: 特定のユーザー取得
@app.get("/users/{user_id}", response_model=dict)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        print(f"ユーザー {user_id} が見つかりません。")
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}

# エンドポイント: ユーザー削除
@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        print(f"ユーザー {user_id} が見つかりません。")
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    print(f"ユーザー {user_id} を削除しました。")
    return {"detail": f"User {user_id} deleted"}

@app.get("/addresses/")
async def get_addresses(zip_codes: List[str] = Query(
        ...,  # 必須
        example=["0600000"]  # 例を追加
    )
):
    tasks = [fetch_address(zip_code) for zip_code in zip_codes]
    results = await asyncio.gather(*tasks)
    return results

app.include_router(books_router.router)

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

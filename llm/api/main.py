import config as config
import asyncio
from typing import List
from api.models import user_model
from api.routers import books_router, memos_router, users_router
from api.schemas.zip_schemas import fetch_address
from api.services.translate import translate_text
from api.services.weather import compiled
from api.database import async_engine

import uvicorn
import logging

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from langserve import add_routes

chain = translate_text(
    llm="gpt-4o-mini",
)


# 非同期でのテーブル作成用の関数を追加
async def create_all_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(user_model.Base.metadata.create_all)

app = FastAPI(
    title="LLM Search",
    description="LLM Search",
    version="0.0.1",
)

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

@app.get("/addresses/")
async def get_addresses(zip_codes: List[str] = Query(
        ...,  # 必須
        examples=["0600000"]  # 例を追加
    )):
    tasks = [fetch_address(zip_code) for zip_code in zip_codes]
    results = await asyncio.gather(*tasks)
    return results


app.include_router(users_router.router)
app.include_router(books_router.router)
app.include_router(memos_router.router)

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

# CORSミドルウェアの追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    # compiled.get_graph().print_ascii()
    asyncio.run(create_all_tables())
    uvicorn.run(app, host="localhost", port=8000)

import config
# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
# import os

# ベースクラスを作成
Base = declarative_base()

# DBファイル作成
# base_dir = os.path.dirname(__file__)

# SQLiteデータベースのURLを設定
## DATABASE_URL = "sqlite:///" + os.path.join(base_dir, "fastapi_app.db")

# TursoのデータベースURLを設定
# DATABASE_URL = f"sqlite+{config.TURSO_DATABASE_URL}/?authToken={config.TURSO_AUTH_TOKEN}&secure=true"

# # SQLiteデータベースのエンジンを作成
# engine = create_engine(
#     DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)
# # セッションローカルを作成
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # データベースセッションの依存関係
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# 非同期エンジンとセッションを作成
ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

async def get_db():
    async with async_session() as session:
        yield session

import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ベースクラスを作成
Base = declarative_base()

# DBファイル作成
base_dir = os.path.dirname(__file__)

# SQLiteデータベースのURLを設定
DATABASE_URL = "sqlite:///" + os.path.join(base_dir, "fastapi_app.db")

# SQLiteデータベースのエンジンを作成
engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)
# セッションローカルを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from config import TURSO_DATABASE_URL, TURSO_AUTH_TOKEN
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ベースクラスを作成
Base = declarative_base()

# TursoのデータベースURLを設定
DATABASE_URL = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

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

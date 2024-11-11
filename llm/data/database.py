import config as config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ベースクラスを作成
Base = declarative_base()

# DBファイル作成
base_dir = os.path.dirname(__file__)

# SQLiteデータベースのURLを設定
## DATABASE_URL = "sqlite:///" + os.path.join(base_dir, "fastapi_app.db")

# TursoのデータベースURLを設定
DATABASE_URL = f"sqlite+{config.TURSO_DATABASE_URL}/?authToken={config.TURSO_AUTH_TOKEN}&secure=true"

# SQLiteデータベースのエンジンを作成
engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)

# セッションローカルを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
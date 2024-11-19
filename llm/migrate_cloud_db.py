from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from sqlalchemy.exc import InternalError, OperationalError
from sqlalchemy import create_engine, text

from api.database import Base
from api.models.book_model import Book  # インポートしてテーブルを登録
from api.models.user_model import User  # インポートしてテーブルを登録

# データベースのURLを設定(非同期化しない)
DB_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?charset=utf8"
)
DEMO_DB_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/demo?charset=utf8"
)

engine = create_engine(DEMO_DB_URL, echo=True)

def database_exists():
    # 接続を試みることでdemoデータベースの存在を確認
    try:
        engine.connect()
        return True
    except (OperationalError, InternalError) as e:
        print(e)
        print("database does not exist")
        return False

def create_database():
    if not database_exists():
        # demoデータベースが存在しなければ作成
        root = create_engine(DB_URL, echo=True)
        with root.connect() as conn:
            conn.execute(text("CREATE DATABASE demo"))
        print("created database")
    # DBモデルをもとにテーブルを作成
    Base.metadata.create_all(bind=engine)
    print("created tables")

if __name__ == "__main__":
    create_database()
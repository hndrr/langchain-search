from sqlalchemy import create_engine

from api.database import Base
from api.models.book_model import Book  # インポートしてテーブルを登録
from api.models.user_model import User  # インポートしてテーブルを登録

# データベースのURLを設定(非同期化しない)
DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    # テーブルを削除して再作成
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
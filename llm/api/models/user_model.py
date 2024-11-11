from sqlalchemy import Column, Integer, String
from data.database import Base

# モデルクラスと、テーブル定義をマッピングさせる

# ユーザモデル
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

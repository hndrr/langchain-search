from sqlalchemy import Column, Integer, String
from api.database import Base

# モデルクラスと、テーブル定義をマッピングさせる

# ユーザモデル
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

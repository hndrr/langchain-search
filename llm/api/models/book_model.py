from sqlalchemy import Column, Float, Integer, String
from api.database import Base

# モデルクラスと、テーブル定義をマッピングさせる

# ブックモデル
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    category = Column(String(255), index=True, nullable=False)
    publish_year = Column(Integer, nullable=True)  # 任意のフィールド
    price = Column(Float, nullable=False)  # 必須のフィールド

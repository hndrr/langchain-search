from api.models.user_model import User
from api.database import Base, SessionLocal, engine
from sqlalchemy import select

# # データベースの初期化
# def init_db():
#     print("データベースの初期化を開始します。")
#     # 既存のテーブルを削除
#     Base.metadata.drop_all(bind=engine)
#     print("既存のテーブルを削除しました。")
#     # テーブルを作成
#     Base.metadata.create_all(bind=engine)
#     print("新しいテーブルを作成しました。")

# ユーザー追加関数
def add_user(name):
    print(f"{name} をデータベースに追加します。")
    with SessionLocal() as session:
        user = User(name=name)
        session.add(user)
        session.commit()
        print(f"{name} をデータベースに追加しました。")

# ユーザー取得関数
def get_users():
    print("データベースからユーザーを取得します。")
    with SessionLocal() as session:
        result = session.execute(select(User))
        users = result.scalars().all()
        print("ユーザーの取得が完了しました。")
        return users

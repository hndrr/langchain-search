from pydantic import BaseModel

# Userクラス
# ユーザのIDと名前を属性として持つ
class User(BaseModel):
    id: int
    name: str

# ダミーデータベースとして機能するユーザリスト
user_list = [
    User(id=1, name="内藤"),
    User(id=2, name="辻"),
    User(id=3, name="鷹木")
]

# 指定されたユーザIDに対応するユーザを
# user_listから検索する関数
# 引数：ユーザID (整数)
# 戻り値：UserオブジェクトまたはNone (見つからない場合)
def get_user(user_id: int) -> User | None:
    for user in user_list:
        if user.id == user_id:
            # 指定されたIDを持つユーザが見つかった場合
            # そのユーザを返す
            return user
    # ユーザが見つからない場合はNoneを返す
    return None
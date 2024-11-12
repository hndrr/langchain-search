import logging
from api.database import get_db
from api.models.user_model import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()

# エンドポイント: ユーザー作成
@router.post("/users/", response_model=dict)
def create_user(name: str, db: Session = Depends(get_db)):  # `next(get_db())` から `Depends(get_db)` に変更
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"ユーザー {name} をデータベースに追加しました。")
    return {"id": user.id, "name": user.name}

# エンドポイント: 全ユーザー取得
@router.get("/users/", response_model=list)
def read_users(db: Session = Depends(get_db)):  # `Depends`で依存関係を設定
    users = db.execute(select(User)).scalars().all()
    print("全ユーザーを取得しました。")
    return [{"id": user.id, "name": user.name} for user in users]

# エンドポイント: 特定のユーザー取得
@router.get("/users/{user_id}", response_model=dict)
def read_user(user_id: int, db: Session = Depends(get_db)):
    logging.debug(f"ユーザ情報取得: user_id={user_id}")
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        logging.error(f"ユーザ情報が見つかりません: user_id={user_id}")
        print(f"ユーザー {user_id} が見つかりません。")
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}

# エンドポイント: ユーザー削除
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        print(f"ユーザー {user_id} が見つかりません。")
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    print(f"ユーザー {user_id} を削除しました。")
    return {"detail": f"User {user_id} deleted"}
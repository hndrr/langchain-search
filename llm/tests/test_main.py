import pytest # type: ignore
import pytest_asyncio # type: ignore
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.database import get_db, Base
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client() -> AsyncClient: # type: ignore
    # 非同期対応したDB接続用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    # クエリパラメータとして name を送信
    response = await async_client.post("/users/?name=テストユーザー")
    
    # ステータスコードの検証
    assert response.status_code == 200, f"レスポンス: {response.json()}"
    
    # レスポンス内容の検証
    data = response.json()
    assert "id" in data
    assert data["name"] == "テストユーザー"

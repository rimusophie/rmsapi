import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import starlette.status

from api.db import get_db, Base
from api.main import app

ASYNC_DB_URL = "mysql+aiomysql://root:root@db:3306/rms_test?charset=utf8"

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # 非同期対応したDB接続用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo = True)
    async_session = sessionmaker(
        autocommit = False, autoflush = False, bind = async_engine, class_ = AsyncSession
    )

    # テスト用にオンメモリのSQLiteテーブルを初期化(関数ごとにリセット)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    #async with AsyncClient(app = app, base_url = "http://localhost:8000") as client:
    async with AsyncClient(transport = ASGITransport(app = app), base_url = "http://localhost:8000") as client:
        yield client

# blog_categoryテスト
@pytest.mark.asyncio
async def test_blog_category(async_client):
    # 作成
    response = await async_client.post("/blog_categories", json = {"name": "aaaa"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["name"] == "aaaa"

    # 取得
    response = await async_client.get("/blog_categories")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["name"] == "aaaa"

    # 更新
    id = response_obj[0]["id"]
    url = f"/blog_categories/{id}"
    response = await async_client.put(url, json = {"name": "bbbb"})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["id"] == id
    assert response_obj["name"] == "bbbb"

    # 削除
    id = response_obj["id"]
    response = await async_client.delete(url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj == None
    
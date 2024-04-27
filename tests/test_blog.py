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

# blogテスト
@pytest.mark.asyncio
async def test_blog(async_client):
    # blog_category作成
    response = await async_client.post("/blog_categories", json = {"name": "aaaa"})
    response_obj = response.json()
    blog_category_id_1 = response_obj["id"]

    response = await async_client.post("/blog_categories", json = {"name": "bbbb"})
    response_obj = response.json()
    blog_category_id_2 = response_obj["id"]

    # 作成
    response = await async_client.post(
        "/blogs", 
        json = {
            "title": "aaaa", 
            "blog_category_id": blog_category_id_1, 
            "filename": "aaa.html",
            "updated_date": "2024-04-01"
        }
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "aaaa"
    assert response_obj["blog_category_id"] == blog_category_id_1
    assert response_obj["filename"] == "aaa.html"
    assert response_obj["updated_date"] == "2024-04-01"

    # 取得
    response = await async_client.get("/blogs")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "aaaa"
    assert response_obj[0]["blog_category_id"] == blog_category_id_1
    assert response_obj[0]["filename"] == "aaa.html"
    assert response_obj[0]["updated_date"] == "2024-04-01"

    # 更新
    id = response_obj[0]["id"]
    url = f"/blogs/{id}"
    response = await async_client.put(
        url, 
        json = {
            "title": "bbbb",
            "blog_category_id": blog_category_id_2, 
            "filename": "bbb.html",
            "updated_date": "2024-04-02"
        }
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["title"] == "bbbb"
    assert response_obj["blog_category_id"] == blog_category_id_2
    assert response_obj["filename"] == "bbb.html"
    assert response_obj["updated_date"] == "2024-04-02"

    # 削除
    id = response_obj["id"]
    response = await async_client.delete(url)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj == None
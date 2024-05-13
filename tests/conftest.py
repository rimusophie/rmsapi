import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy import create_engine

from api.db import get_db, get_engine, get_env_info, Base
from api.main import app
from tests.env import ASYNC_DB_URL, DB_URL, DB_HOST, DB_NAME, DB_PORT

@pytest_asyncio.fixture(autouse = True, scope = "session")
async def init_test():
    # 非同期対応したDB接続用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo = True)

    # テスト用にテーブルを初期化
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await async_engine.dispose()

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # 非同期対応したDB接続用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo = True)
    async_session = sessionmaker(
        autocommit = False, autoflush = False, bind = async_engine, class_ = AsyncSession
    )

    # テーブルをTRUNCATE
    async with async_engine.connect() as conn:
        await conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        for table in Base.metadata.sorted_tables:
            await conn.execute(text(f"TRUNCATE TABLE {table.name};"))
        await conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(transport = ASGITransport(app = app), base_url = "http://localhost:8000") as client:
        yield client

    app.dependency_overrides.clear()

    # event_loopエラーが出るため明示的に後始末をする
    await async_engine.dispose()

@pytest_asyncio.fixture
async def async_client_engine() -> AsyncClient:
    def get_test_engine():
        conn = create_engine(DB_URL, echo = True)
        try:
            yield conn
        finally:
            conn.dispose()

    # データベース情報を取得
    def get_test_env_info():
        ret: dict = {
            "host": DB_HOST,
            "name": DB_NAME,
            "port": DB_PORT
        }
        return ret

    app.dependency_overrides[get_engine] = get_test_engine
    app.dependency_overrides[get_env_info] = get_test_env_info

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(transport = ASGITransport(app = app), base_url = "http://localhost:8000") as client:
        yield client

    app.dependency_overrides.clear()
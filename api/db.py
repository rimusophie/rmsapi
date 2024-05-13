from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from api.env import ASYNC_DB_URL, DB_URL, DB_HOST, DB_NAME, DB_PORT

async_engine = create_async_engine(ASYNC_DB_URL, echo = True)
async_session = sessionmaker(autocommit = False, autoflush = False, bind = async_engine, class_ = AsyncSession)

engine = create_engine(DB_URL, echo = True)

Base = declarative_base()

# セッションを取得
async def get_db():
    async with async_session() as session:
        yield session

# エンジンを取得
def get_engine():
    return engine

# データベース情報を取得
def get_env_info():
    ret: dict = {
        "host": DB_HOST,
        "name": DB_NAME,
        "port": DB_PORT
    }
    return ret
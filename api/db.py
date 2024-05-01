from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from api.env import ASYNC_DB_URL
from api.env import DB_URL

async_engine = create_async_engine(ASYNC_DB_URL, echo = True)
async_session = sessionmaker(autocommit = False, autoflush = False, bind = async_engine, class_ = AsyncSession)

engine = create_engine(DB_URL, echo = True)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

def get_engine():
    return engine
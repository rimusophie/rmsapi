#from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

#DB_URL = "mysql+pymysql://root:root@db:3306/rms?charset=utf8"
ASYNC_DB_URL = "mysql+aiomysql://root:root@db:3306/rms?charset=utf8"

#db_engine = create_engine(DB_URL, echo = True)
#db_session = sessionmaker(autocommit = False, autoflush = False, bind = db_engine)
async_engine = create_async_engine(ASYNC_DB_URL, echo = True)
async_session = sessionmaker(autocommit = False, autoflush = False, bind = async_engine, class_ = AsyncSession)

Base = declarative_base()

#def get_db():
#    with db_session() as session:
#        yield session
async def get_db():
    async with async_session() as session:
        yield session
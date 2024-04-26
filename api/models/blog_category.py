from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text
from api.db import Base
from api.models.blog import Blog

class BlogCategory(Base):
    __tablename__ = "blog_categories"

    # id
    id = Column(Integer, primary_key = True, autoincrement = True)

    # 名称
    name = Column(String(100))

    # 更新日時(システム管理)
    updated_at = Column(Timestamp, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

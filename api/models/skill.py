from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text
from api.db import Base

class Skill(Base):
    __tablename__ = "skills"

    # id
    id = Column(Integer, primary_key = True, autoincrement = True)

    # 名称
    name = Column(String(100))

    # カテゴリ(1=資格/2=業務経験/99=その他/0=未指定)
    category = Column(Integer, comment="1=資格/2=業務経験/99=その他")

    # 更新日時(システム管理)
    updated_at = Column(Timestamp, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="システム管理")

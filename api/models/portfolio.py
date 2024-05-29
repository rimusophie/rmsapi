from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text
from api.db import Base

class Portfolio(Base):
    __tablename__ = "portfolios"

    # id
    id = Column(Integer, primary_key = True, autoincrement = True)

    # 案件名
    name = Column(String(200))

    # 備考
    remark = Column(String(500))

    # 更新日時(システム管理)
    updated_at = Column(Timestamp, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="システム管理")

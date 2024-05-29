from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text
from api.db import Base

class PortfolioSkill(Base):
    __tablename__ = "portfolio_skills"

    # id
    id = Column(Integer, primary_key = True, autoincrement = True)

    # portfolios.id
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="SET NULL", onupdate="CASCADE"))

    # skills.id
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="SET NULL", onupdate="CASCADE"))

    # 更新日時(システム管理)
    updated_at = Column(Timestamp, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment="システム管理")

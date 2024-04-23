from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
from sqlalchemy.sql.expression import text
from api.db import Base

class Blog(Base):
    __tablename__ = "blogs"

    # id
    id = Column(Integer, primary_key = True, autoincrement = True)

    # タイトル
    title = Column(String(200))

    # カテゴリ
    blog_category_id = Column(Integer, ForeignKey("blog_categories.id", ondelete="SET NULL", onupdate="CASCADE"))

    # ファイル名(拡張子を含む)
    filename = Column(String(250))

    # 更新日(表示上の)
    updated_date = Column(Date)

    # 更新日時(システム管理)
    updated_at = Column(Timestamp, server_default = text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

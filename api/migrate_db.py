from sqlalchemy import create_engine

from api.models.blog import Base as blog_base
from api.models.blog_category import Base as blog_category_base

DB_URL = "mysql+pymysql://root:root@db:3306/rms_test?charset=utf8"
engine = create_engine(DB_URL, echo = True)

def reset_database():
    # 削除
    blog_base.metadata.drop_all(bind = engine)
    blog_category_base.metadata.drop_all(bind = engine)

    # 作成
    blog_category_base.metadata.create_all(bind = engine)
    blog_base.metadata.create_all(bind = engine)

if __name__ == "__main__":
    reset_database()
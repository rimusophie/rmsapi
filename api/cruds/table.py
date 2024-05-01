from sqlalchemy import inspect

from api.env import DB_URL

# 一覧取得
def get_tables(engine) -> list[tuple[str]]:
    inspector = inspect(engine)

    return inspector.get_table_names()
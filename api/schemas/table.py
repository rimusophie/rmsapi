from pydantic import BaseModel

# 取得
class Table(BaseModel):
    name: str

class DBInfo(BaseModel):
    host: str
    name: str
    port: int
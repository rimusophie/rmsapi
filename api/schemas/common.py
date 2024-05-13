from pydantic import BaseModel

# 件数
class CountModel(BaseModel):
    count: int

# keyvalue
class KeyValueModel(BaseModel):
    id: int
    name: str
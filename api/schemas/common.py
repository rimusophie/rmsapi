from pydantic import BaseModel

# 件数
class CountModel(BaseModel):
    count: int
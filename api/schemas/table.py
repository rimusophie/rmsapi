from pydantic import BaseModel, Field

# 取得
class Table(BaseModel):
    name: str = Field("blogs", max_length = 64)

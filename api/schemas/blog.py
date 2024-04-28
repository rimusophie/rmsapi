from pydantic import BaseModel, Field, ConfigDict
from datetime import date

# 共通
class BlogBase(BaseModel):
    title: str = Field("", max_length = 200)
    blog_category_id: int = Field(None)
    filename: str = Field("", max_length = 250)
    updated_date: date = Field(None)

# 更新時
class BlogCreate(BlogBase):
    pass

# 更新時のレスポンス
class BlogCreateResponse(BlogCreate):
    id: int

    model_config = ConfigDict(from_attributes = True)

# 取得
class Blog(BlogBase):
    id: int

    model_config = ConfigDict(from_attributes = True)
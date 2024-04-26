from pydantic import BaseModel, Field
from datetime import date

# 共通
class BlogBase(BaseModel):
    title: str = Field("", max_length = 200, example = "日常")
    blog_category_id: int = Field(None)
    filename: str = Field("", max_length = 250, example = "test.html")
    updated_date: date = Field(None)

# 更新時
class BlogCreate(BlogBase):
    pass

# 更新時のレスポンス
class BlogCreateResponse(BlogCreate):
    id: int

    class Config:
        orm_mode = True

# 取得
class Blog(BlogBase):
    id: int

    class Config:
        orm_mode = True
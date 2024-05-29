from pydantic import BaseModel, Field, ConfigDict
from datetime import date

# レスポンス
class BlogResponse(BaseModel):
    id: int
    title: str | None
    blog_category_id: int | None
    filename: str | None
    updated_date: date | None

    model_config = ConfigDict(from_attributes = True)

# リクエスト
class BlogRequest(BaseModel):
    title: str | None = Field(default = None, max_length = 200)
    blog_category_id: int | None = Field(default = None)
    filename: str | None = Field(default = None, max_length = 250)
    updated_date: date | None = Field(default = None)
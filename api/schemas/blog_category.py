from pydantic import BaseModel, Field, ConfigDict

# レスポンス
class BlogCategoryResponse(BaseModel):
    id: int
    name: str | None

    model_config = ConfigDict(from_attributes = True)

# リクエスト
class BlogCategoryRequest(BaseModel):
    name: str | None = Field(default = None, max_length = 100)
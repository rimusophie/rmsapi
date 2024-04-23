from pydantic import BaseModel, Field

# 共通
class BlogCategoryBase(BaseModel):
    name: str = Field("", example="日常")

# 更新時
class BlogCategoryCreate(BlogCategoryBase):
    pass

# 更新時のレスポンス
class BlogCategoryCreateResponse(BlogCategoryCreate):
    id: int

    class Config:
        orm_mode = True

# 取得
class BlogCategory(BlogCategoryBase):
    id: int

    class Config:
        orm_mode = True
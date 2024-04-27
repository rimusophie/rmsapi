from pydantic import BaseModel, Field, ConfigDict

# 共通
class BlogCategoryBase(BaseModel):
    name: str = Field("", max_length = 100)

# 更新時
class BlogCategoryCreate(BlogCategoryBase):
    pass

# 更新時のレスポンス
class BlogCategoryCreateResponse(BlogCategoryCreate):
    id: int

    """ class Config:
        orm_mode = True """
    model_config = ConfigDict(from_attributes = True)

# 取得
class BlogCategory(BlogCategoryBase):
    id: int

    """ class Config:
        orm_mode = True """
    model_config = ConfigDict(from_attributes = True)
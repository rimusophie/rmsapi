from pydantic import BaseModel, Field

class BlogCategoryBase(BaseModel):
    name: str = Field("", example="日常")

class BlogCategoryCreate(BlogCategoryBase):
    pass

class BlogCategoryCreateResponse(BlogCategoryCreate):
    id: int

    class Config:
        orm_mode = True

class BlogCategory(BlogCategoryBase):
    id: int

    class Config:
        orm_mode = True
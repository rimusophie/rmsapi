from fastapi import APIRouter

import api.schemas.blog_category as blog_category_schema

router = APIRouter()

# 一覧取得
@router.get("/blog_categories", response_model = list[blog_category_schema.BlogCategory])
async def list_blog_categories():
    return [blog_category_schema.BlogCategory(id = 1, name = "テスト")]

# 詳細取得
@router.get("/blog_categories/{id}", response_model = blog_category_schema.BlogCategory)
async def detail_blog_category():
    return blog_category_schema.BlogCategory(id = 2, name = "テスト2")

# 追加
@router.post("/blog_categories", response_model = blog_category_schema.BlogCategoryCreateResponse)
async def create_blog_category(body: blog_category_schema.BlogCategoryCreate):
    return blog_category_schema.BlogCategoryCreateResponse(id = 1, **body.dict())

# 更新
@router.put("/blog_categories/{id}", response_model = blog_category_schema.BlogCategoryCreateResponse)
async def update_blog_category(id: int, body: blog_category_schema.BlogCategoryCreate):
    return blog_category_schema.BlogCategoryCreateResponse(id = id, **body.dict())

# 削除
@router.delete("/blog_categories/{id}", response_model = None)
async def delete_blog_category(id: int):
    return
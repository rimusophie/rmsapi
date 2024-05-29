from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.blog_category as crud
import api.schemas.blog_category as schema
import api.schemas.common as schema_common
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/blog_categories", response_model = list[schema.BlogCategoryResponse])
async def list_blog_categories(db: AsyncSession = Depends(get_db), page: int = Query(default = 1, gt = 0), limit: int = Query(default = 50, gt = 0, le = 50)):
    return await crud.get_blog_categories(db, page = page, limit = limit)

# 一覧取得(idとnameのみ)
@router.get("/blog_categories_keyvalue", response_model = list[schema_common.KeyValueModel])
async def list_blog_categories_keyvalue(db: AsyncSession = Depends(get_db)):
    return await crud.get_blog_categories_keyvalue(db)

# 詳細取得
@router.get("/blog_categories/{id}", response_model = schema.BlogCategoryResponse)
async def detail_blog_category(id: int, db: AsyncSession = Depends(get_db)):
    blog_category = await crud.get_blog_category(db, id = id)

    if blog_category is None:
        raise HTTPException(status_code = 404, detail = "BlogCategory not found")

    return blog_category

# 追加
@router.post("/blog_categories", response_model = schema.BlogCategoryResponse)
async def create_blog_category(body: schema.BlogCategoryRequest, db: AsyncSession = Depends(get_db)):
    return await crud.create_blog_category(db, body)

# 更新
@router.put("/blog_categories/{id}", response_model = schema.BlogCategoryResponse)
async def update_blog_category(id: int, body: schema.BlogCategoryRequest, db: AsyncSession = Depends(get_db)):
    blog_category = await crud.get_blog_category(db, id = id)

    if blog_category is None:
        raise HTTPException(status_code = 404, detail = "BlogCategory not found")
    
    return await crud.update_blog_category(db, body, data=blog_category)

# 削除
@router.delete("/blog_categories/{id}", response_model = None)
async def delete_blog_category(id: int, db: AsyncSession = Depends(get_db)):
    blog_category = await crud.get_blog_category(db, id = id)

    if blog_category is None:
        raise HTTPException(status_code = 404, detail = "BlogCategory not found")

    return await crud.delete_blog_category(db, data=blog_category)

# 件数取得
@router.get("/blog_categories_count", response_model = schema_common.CountModel)
async def count_blog_category(db: AsyncSession = Depends(get_db)):
    count = await crud.count_blog_category(db)
    ret = schema_common.CountModel(count = count)

    return ret
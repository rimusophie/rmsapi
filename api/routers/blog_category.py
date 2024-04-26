from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.blog_category as crud
import api.schemas.blog_category as schema
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/blog_categories", response_model = list[schema.BlogCategory])
async def list_blog_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_blog_categories(db)

# 詳細取得
@router.get("/blog_categories/{id}", response_model = schema.BlogCategory)
async def detail_blog_category(id: int, db: AsyncSession = Depends(get_db)):
    blog_category = await crud.get_blog_category(db, id = id)

    if blog_category is None:
        raise HTTPException(status_code = 404, detail = "BlogCategory not found")

    return blog_category

# 追加
@router.post("/blog_categories", response_model = schema.BlogCategoryCreateResponse)
async def create_blog_category(body: schema.BlogCategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_blog_category(db, body)

# 更新
@router.put("/blog_categories/{id}", response_model = schema.BlogCategoryCreateResponse)
async def update_blog_category(id: int, body: schema.BlogCategoryCreate, db: AsyncSession = Depends(get_db)):
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
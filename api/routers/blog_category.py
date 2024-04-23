from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.cruds.blog_categories as crud
import api.schemas.blog_category as schema
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/blog_categories", response_model = list[schema.BlogCategory])
async def list_blog_categories(db: Session = Depends(get_db)):
    return crud.get_blog_categories(db)

# 詳細取得
@router.get("/blog_categories/{id}", response_model = schema.BlogCategory)
async def detail_blog_category(id: int, db: Session = Depends(get_db)):
    blog_category = crud.get_blog_category(db, id = id)

    if blog_category is None:
        raise HTTPException(status_code = 404, detail = "BlogCategory not found")

    return blog_category

# 追加
@router.post("/blog_categories", response_model = schema.BlogCategoryCreateResponse)
async def create_blog_category(body: schema.BlogCategoryCreate, db: Session = Depends(get_db)):
    return crud.create_blog_category(db, body)

# 更新
@router.put("/blog_categories/{id}", response_model = schema.BlogCategoryCreateResponse)
async def update_blog_category(id: int, body: schema.BlogCategoryCreate, db: Session = Depends(get_db)):
    blog_category = crud.get_blog_category(db, id = id)

    if blog_category is None:
        raise HTTPException(status_code = 404, detail = "BlogCategory not found")
    
    return crud.update_blog_category(db, body, original=blog_category)

# 削除
@router.delete("/blog_categories/{id}", response_model = None)
async def delete_blog_category(id: int, db: Session = Depends(get_db)):
    blog_category = crud.get_blog_category(db, id = id)

    if blog_category is None:
        raise HTTPException(status_code = 404, detail = "BlogCategory not found")

    return crud.delete_blog_category(db, original=blog_category)
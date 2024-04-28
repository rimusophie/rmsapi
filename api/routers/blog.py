from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.blog as crud
import api.schemas.blog as schema
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/blogs", response_model = list[schema.Blog])
async def list_blogs(db: AsyncSession = Depends(get_db)):
    return await crud.get_blogs(db)

# 詳細取得
@router.get("/blogs/{id}", response_model = schema.Blog)
async def detail_blog(id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, id = id)

    if blog is None:
        raise HTTPException(status_code = 404, detail = "Blog not found")

    return blog

# 追加
@router.post("/blogs", response_model = schema.BlogCreateResponse)
async def create_blog(body: schema.BlogCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_blog(db, body)

# 更新
@router.put("/blogs/{id}", response_model = schema.BlogCreateResponse)
async def update_blog(id: int, body: schema.BlogCreate, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, id = id)

    if blog is None:
        raise HTTPException(status_code = 404, detail = "Blog not found")
    
    return await crud.update_blog(db, body, data=blog)

# 削除
@router.delete("/blogs/{id}", response_model = None)
async def delete_blog(id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, id = id)

    if blog is None:
        raise HTTPException(status_code = 404, detail = "Blog not found")

    return await crud.delete_blog(db, data=blog)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.blog as crud
import api.schemas.blog as schema
import api.schemas.common as schema_common
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/blogs", response_model = list[schema.BlogResponse])
async def list_blogs(db: AsyncSession = Depends(get_db), page: int = Query(default = 1, gt = 0), limit: int = Query(default = 50, gt = 0, le = 50)):
    return await crud.get_blogs(db, page = page, limit = limit)

# 詳細取得
@router.get("/blogs/{id}", response_model = schema.BlogResponse)
async def detail_blog(id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, id = id)

    if blog is None:
        raise HTTPException(status_code = 404, detail = "Blog not found")

    return blog

# 追加
@router.post("/blogs", response_model = schema.BlogResponse)
async def create_blog(body: schema.BlogRequest, db: AsyncSession = Depends(get_db)):
    return await crud.create_blog(db, body)

# 更新
@router.put("/blogs/{id}", response_model = schema.BlogResponse)
async def update_blog(id: int, body: schema.BlogRequest, db: AsyncSession = Depends(get_db)):
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

# 件数取得
@router.get("/blogs_count", response_model = schema_common.CountModel)
async def count_blog_category(db: AsyncSession = Depends(get_db)):
    count = await crud.count_blog(db)
    ret = schema_common.CountModel(count = count)

    return ret
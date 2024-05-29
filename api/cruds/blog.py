from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from datetime import date
import api.models.blog as model
import api.models.blog_category as model_blog_category
import api.schemas.blog as schema

# 登録
async def create_blog(db: AsyncSession, data: schema.BlogRequest) -> model.Blog:
    ret = model.Blog(
        title = data.title, 
        blog_category_id = data.blog_category_id, 
        filename = data.filename,
        updated_date = data.updated_date
    )
    db.add(ret)
    await db.commit()
    await db.refresh(ret)
    return ret

# 一覧取得
async def get_blogs(db: AsyncSession, page: int, limit: int) -> list[tuple[int, str, int, str, date]]:
    ret: Result = await db.execute(
        select(
            model.Blog.id,
            model.Blog.title,
            model.Blog.blog_category_id,
            model_blog_category.BlogCategory.name,
            model.Blog.filename,
            model.Blog.updated_date
        ).outerjoin(model_blog_category.BlogCategory, model.Blog.blog_category_id == model_blog_category.BlogCategory.id)
        .order_by(model.Blog.id)
        .limit(limit).offset((page - 1) * limit)
    )
    return ret.all()

# 詳細取得
async def get_blog(db: AsyncSession, id: int) -> model.Blog | None:
    ret: Result = await db.execute(
        select(
            model.Blog
        ).outerjoin(
            model_blog_category.BlogCategory, model.Blog.blog_category_id == model_blog_category.BlogCategory.id
        ).filter(model.Blog.id == id)
    )
    return ret.scalars().first()

# 更新
async def update_blog(db: AsyncSession, new_data: schema.BlogRequest, data: model.Blog) -> model.Blog:
    data.title = new_data.title
    data.blog_category_id = new_data.blog_category_id
    data.filename = new_data.filename
    data.updated_date = new_data.updated_date
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data

# 削除
async def delete_blog(db: AsyncSession, data: model.Blog) -> None:
    await db.delete(data)
    await db.commit()

# 件数取得
async def count_blog(db: AsyncSession) -> int:
    ret: Result = await db.execute(
        func.count(model.Blog.id)
    )
    
    return ret.scalar()
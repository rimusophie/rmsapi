from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.blog_category as model
import api.schemas.blog_category as schema

# 登録
async def create_blog_category(db: AsyncSession, data: schema.BlogCategoryCreate) -> model.BlogCategory:
    #ret = model.BlogCategory(**data.dict())
    ret = model.BlogCategory(name = data.name)
    db.add(ret)
    await db.commit()
    await db.refresh(ret)
    return ret

# 一覧取得
async def get_blog_categories(db: AsyncSession) -> list[tuple[int, str]]:
    ret: Result = await db.execute(
        select(
            model.BlogCategory.id,
            model.BlogCategory.name
        )
    )
    return ret.all()

# 詳細取得
async def get_blog_category(db: AsyncSession, id: int) -> model.BlogCategory | None:
    ret: Result = await db.execute(
        select(model.BlogCategory).filter(model.BlogCategory.id == id)
    )
    return ret.scalars().first()

# 更新
async def update_blog_category(db: AsyncSession, new_data: schema.BlogCategory, data: model.BlogCategory) -> model.BlogCategory:
    data.name = new_data.name
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data

# 削除
async def delete_blog_category(db: AsyncSession, data: model.BlogCategory) -> None:
    await db.delete(data)
    await db.commit()
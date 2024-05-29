from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from datetime import date
import api.models.portfolio as model
import api.models.blog_category as model_blog_category
import api.schemas.portfolio as schema

# 登録
async def create_portfolio(db: AsyncSession, data: schema.PortfolioRequest) -> model.Portfolio:
    ret = model.Portfolio(
        name = data.name, 
        remark = data.remark, 
    )
    db.add(ret)
    await db.commit()
    await db.refresh(ret)
    return ret

# 一覧取得
async def get_portfolios(db: AsyncSession, page: int, limit: int) -> list[tuple[int, str, str]]:
    ret: Result = await db.execute(
        select(
            model.Portfolio.id,
            model.Portfolio.name,
            model.Portfolio.remark,
        )
        .order_by(model.Portfolio.id)
        .limit(limit).offset((page - 1) * limit)
    )
    return ret.all()

# 詳細取得
async def get_portfolio(db: AsyncSession, id: int) -> model.Portfolio | None:
    ret: Result = await db.execute(
        select(
            model.Portfolio
        ).filter(model.Portfolio.id == id)
    )
    return ret.scalars().first()

# 更新
async def update_portfolio(db: AsyncSession, new_data: schema.PortfolioRequest, data: model.Portfolio) -> model.Portfolio:
    data.name = new_data.name
    data.remark = new_data.remark
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data

# 削除
async def delete_portfolio(db: AsyncSession, data: model.Portfolio) -> None:
    await db.delete(data)
    await db.commit()

# 件数取得
async def count_portfolio(db: AsyncSession) -> int:
    ret: Result = await db.execute(
        func.count(model.Portfolio.id)
    )
    
    return ret.scalar()
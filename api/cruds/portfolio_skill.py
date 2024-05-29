from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from datetime import date
import api.models.portfolio_skill as model
import api.models.blog_category as model_blog_category
import api.schemas.portfolio_skill as schema

# 登録
async def create_portfolio_skill(db: AsyncSession, data: schema.PortfolioSkillRequest) -> model.PortfolioSkill:
    ret = model.PortfolioSkill(
        portfolio_id = data.portfolio_id, 
        skill_id = data.skill_id, 
    )
    
    db.add(ret)
    await db.commit()
    await db.refresh(ret)
    return ret

# 一覧取得
async def get_portfolio_skills(db: AsyncSession, portfolio_id: int | None, skill_id: int | None, page: int, limit: int) -> list[tuple[int, int, int]]:
    # 絞りなし
    if(portfolio_id == None and skill_id == None):
        return await get_portfolio_skills_all(db = db, page = page, limit = limit)

    # skill_id絞り
    if(portfolio_id == None and skill_id != None):
        return await get_portfolio_skills_skill(db = db, skill_id = skill_id, page = page, limit = limit)
    
    # portfolio_id絞り
    if(portfolio_id != None and skill_id == None):
        return await get_portfolio_skills_portfolio(db = db, portfolio_id = portfolio_id, page = page, limit = limit)
    
    # 全絞り
    ret: Result = await db.execute(
        select(
            model.PortfolioSkill.id,
            model.PortfolioSkill.portfolio_id,
            model.PortfolioSkill.skill_id,
        )
        .filter(model.PortfolioSkill.portfolio_id == portfolio_id, model.PortfolioSkill.skill_id == skill_id)
        .order_by(model.PortfolioSkill.id)
        .limit(limit).offset((page - 1) * limit)
    )
    return ret.all()

# 一覧取得(条件なし)
async def get_portfolio_skills_all(db: AsyncSession, page: int, limit: int) -> list[tuple[int, int, int]]:
    ret: Result = await db.execute(
        select(
            model.PortfolioSkill.id,
            model.PortfolioSkill.portfolio_id,
            model.PortfolioSkill.skill_id,
        )
        .order_by(model.PortfolioSkill.id)
        .limit(limit).offset((page - 1) * limit)
    )
    return ret.all()

# 一覧取得(portfolio_idのみ)
async def get_portfolio_skills_portfolio(db: AsyncSession, portfolio_id: int, page: int, limit: int) -> list[tuple[int, int, int]]:
    ret: Result = await db.execute(
        select(
            model.PortfolioSkill.id,
            model.PortfolioSkill.portfolio_id,
            model.PortfolioSkill.skill_id,
        )
        .filter(model.PortfolioSkill.portfolio_id == portfolio_id)
        .order_by(model.PortfolioSkill.skill_id)
        .limit(limit).offset((page - 1) * limit)
    )
    return ret.all()

# 一覧取得(skill_idのみ)
async def get_portfolio_skills_skill(db: AsyncSession, skill_id: int, page: int, limit: int) -> list[tuple[int, int, int]]:
    ret: Result = await db.execute(
        select(
            model.PortfolioSkill.id,
            model.PortfolioSkill.portfolio_id,
            model.PortfolioSkill.skill_id,
        )
        .filter(model.PortfolioSkill.skill_id == skill_id)
        .order_by(model.PortfolioSkill.portfolio_id)
        .limit(limit).offset((page - 1) * limit)
    )
    return ret.all()

# 詳細取得
async def get_portfolio_skill(db: AsyncSession, id: int) -> model.PortfolioSkill | None:
    ret: Result = await db.execute(
        select(
            model.PortfolioSkill
        ).filter(model.PortfolioSkill.id == id)
    )
    return ret.scalars().first()

# 更新
async def update_portfolio_skill(db: AsyncSession, new_data: schema.PortfolioSkillRequest, data: model.PortfolioSkill) -> model.PortfolioSkill:
    data.portfolio_id = new_data.portfolio_id
    data.skill_id = new_data.skill_id
    
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data

# 削除
async def delete_portfolio_skill(db: AsyncSession, data: model.PortfolioSkill) -> None:
    await db.delete(data)
    await db.commit()

# 件数取得
async def count_portfolio_skill(db: AsyncSession) -> int:
    ret: Result = await db.execute(
        func.count(model.PortfolioSkill.id)
    )
    
    return ret.scalar()
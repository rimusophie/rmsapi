from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pymysql import IntegrityError

import api.cruds.portfolio_skill as crud
import api.schemas.portfolio_skill as schema
import api.schemas.common as schema_common
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/portfolio_skills", response_model = list[schema.PortfolioSkillResponse])
async def list_portfolio_skills(db: AsyncSession = Depends(get_db), portfolio_id: int = Query(default = None, gt = 0), skill_id: int = Query(default = None, gt = 0), page: int = Query(default = 1, gt = 0), limit: int = Query(default = 50, gt = 0, le = 50)):
    return await crud.get_portfolio_skills(db, portfolio_id = portfolio_id, skill_id = skill_id, page = page, limit = limit)

# 詳細取得
@router.get("/portfolio_skills/{id}", response_model = schema.PortfolioSkillResponse)
async def detail_portfolio_skill(id: int, db: AsyncSession = Depends(get_db)):
    portfolio_skill = await crud.get_portfolio_skill(db, id = id)

    if portfolio_skill is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")

    return portfolio_skill

# 追加
@router.post("/portfolio_skills", response_model = schema.PortfolioSkillResponse)
async def create_portfolio_skill(body: schema.PortfolioSkillRequest, db: AsyncSession = Depends(get_db)):
    return await crud.create_portfolio_skill(db, body)

# 更新
@router.put("/portfolio_skills/{id}", response_model = schema.PortfolioSkillResponse)
async def update_portfolio_skill(id: int, body: schema.PortfolioSkillRequest, db: AsyncSession = Depends(get_db)):
    portfolio_skill = await crud.get_portfolio_skill(db, id = id)

    if portfolio_skill is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")
    
    return await crud.update_portfolio_skill(db, body, data=portfolio_skill)

# 削除
@router.delete("/portfolio_skills/{id}", response_model = None)
async def delete_portfolio_skill(id: int, db: AsyncSession = Depends(get_db)):
    portfolio_skill = await crud.get_portfolio_skill(db, id = id)

    if portfolio_skill is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")

    return await crud.delete_portfolio_skill(db, data=portfolio_skill)

# 件数取得
@router.get("/portfolio_skills_count", response_model = schema_common.CountModel)
async def count_portfolio_skill(db: AsyncSession = Depends(get_db)):
    count = await crud.count_portfolio_skill(db)
    ret = schema_common.CountModel(count = count)

    return ret
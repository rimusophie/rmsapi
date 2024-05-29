from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.portfolio as crud
import api.schemas.portfolio as schema
import api.schemas.common as schema_common
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/portfolios", response_model = list[schema.PortfolioResponse])
async def list_portfolios(db: AsyncSession = Depends(get_db), page: int = Query(default = 1, gt = 0), limit: int = Query(default = 50, gt = 0, le = 50)):
    return await crud.get_portfolios(db, page = page, limit = limit)

# 詳細取得
@router.get("/portfolios/{id}", response_model = schema.PortfolioResponse)
async def detail_portfolio(id: int, db: AsyncSession = Depends(get_db)):
    portfolio = await crud.get_portfolio(db, id = id)

    if portfolio is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")

    return portfolio

# 追加
@router.post("/portfolios", response_model = schema.PortfolioResponse)
async def create_portfolio(body: schema.PortfolioRequest, db: AsyncSession = Depends(get_db)):
    return await crud.create_portfolio(db, body)

# 更新
@router.put("/portfolios/{id}", response_model = schema.PortfolioResponse)
async def update_portfolio(id: int, body: schema.PortfolioRequest, db: AsyncSession = Depends(get_db)):
    portfolio = await crud.get_portfolio(db, id = id)

    if portfolio is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")
    
    return await crud.update_portfolio(db, body, data=portfolio)

# 削除
@router.delete("/portfolios/{id}", response_model = None)
async def delete_portfolio(id: int, db: AsyncSession = Depends(get_db)):
    portfolio = await crud.get_portfolio(db, id = id)

    if portfolio is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")

    return await crud.delete_portfolio(db, data=portfolio)

# 件数取得
@router.get("/portfolios_count", response_model = schema_common.CountModel)
async def count_portfolio(db: AsyncSession = Depends(get_db)):
    count = await crud.count_portfolio(db)
    ret = schema_common.CountModel(count = count)

    return ret
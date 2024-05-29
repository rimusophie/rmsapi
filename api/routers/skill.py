from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.skill as crud
import api.schemas.skill as schema
import api.schemas.common as schema_common
from api.db import get_db

router = APIRouter()

# 一覧取得
@router.get("/skills", response_model = list[schema.SkillResponse])
async def list_skills(db: AsyncSession = Depends(get_db), page: int = Query(default = 1, gt = 0), limit: int = Query(default = 50, gt = 0, le = 50)):
    return await crud.get_skills(db, page = page, limit = limit)

# 一覧取得(idとnameのみ)
@router.get("/skills_keyvalue", response_model = list[schema_common.KeyValueModel])
async def list_skills_keyvalue(db: AsyncSession = Depends(get_db)):
    return await crud.get_skills_keyvalue(db)

# 詳細取得
@router.get("/skills/{id}", response_model = schema.SkillResponse)
async def detail_skill(id: int, db: AsyncSession = Depends(get_db)):
    skill = await crud.get_skill(db, id = id)

    if skill is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")

    return skill

# 追加
@router.post("/skills", response_model = schema.SkillResponse)
async def create_skill(body: schema.SkillRequest, db: AsyncSession = Depends(get_db)):
    return await crud.create_skill(db, body)

# 更新
@router.put("/skills/{id}", response_model = schema.SkillResponse)
async def update_skill(id: int, body: schema.SkillRequest, db: AsyncSession = Depends(get_db)):
    skill = await crud.get_skill(db, id = id)

    if skill is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")
    
    return await crud.update_skill(db, body, data=skill)

# 削除
@router.delete("/skills/{id}", response_model = None)
async def delete_skill(id: int, db: AsyncSession = Depends(get_db)):
    skill = await crud.get_skill(db, id = id)

    if skill is None:
        raise HTTPException(status_code = 404, detail = "該当レコードなし")

    return await crud.delete_skill(db, data=skill)

# 件数取得
@router.get("/skills_count", response_model = schema_common.CountModel)
async def count_skill(db: AsyncSession = Depends(get_db)):
    count = await crud.count_skill(db)
    ret = schema_common.CountModel(count = count)

    return ret
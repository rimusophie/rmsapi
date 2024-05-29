from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

import api.models.skill as model
import api.schemas.skill as schema

# 登録
async def create_skill(db: AsyncSession, data: schema.SkillRequest) -> model.Skill:
    ret = model.Skill(
        name = data.name, 
        category = data.category
    )
    db.add(ret)
    await db.commit()
    await db.refresh(ret)
    return ret

# 一覧取得
async def get_skills(db: AsyncSession, page: int, limit: int) -> list[tuple[int, str, int]]:
    ret: Result = await db.execute(
        select(
            model.Skill.id,
            model.Skill.name,
            model.Skill.category
        )
        .order_by(model.Skill.category, model.Skill.id)
        .limit(limit).offset((page - 1) * limit)
    )
    return ret.all()

# 一覧取得(idとnameのみ)
async def get_skills_keyvalue(db: AsyncSession) -> list[tuple[int, str]]:
    # カテゴリ,名称順にする
    ret: Result = await db.execute(
        select(
            model.Skill.id,
            model.Skill.name
        )
        .order_by(model.Skill.category, model.Skill.name)
    )
    return ret.all()

# 詳細取得
async def get_skill(db: AsyncSession, id: int) -> model.Skill | None:
    ret: Result = await db.execute(
        select(model.Skill).filter(model.Skill.id == id)
    )
    return ret.scalars().first()

# 更新
async def update_skill(db: AsyncSession, new_data: schema.SkillRequest, data: model.Skill) -> model.Skill:
    data.name = new_data.name
    data.category = new_data.category
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data

# 削除
async def delete_skill(db: AsyncSession, data: model.Skill) -> None:
    await db.delete(data)
    await db.commit()

# 件数取得
async def count_skill(db: AsyncSession) -> int:
    ret: Result = await db.execute(
        func.count(model.Skill.id)
    )
    
    return ret.scalar()
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.blog_category as model
import api.schemas.blog_category as schema

# 登録
def create_blog_category(db: Session, data: schema.BlogCategoryCreate) -> model.BlogCategory:
    ret = model.BlogCategory(**data.dict())
    db.add(ret)
    db.commit()
    db.refresh(ret)
    return ret

# 一覧取得
def get_blog_categories(db: Session) -> list[tuple[int, str]]:
    ret: Result = db.execute(
        select(
            model.BlogCategory.id,
            model.BlogCategory.name
        )
    )
    return ret.all()

# 詳細取得
def get_blog_category(db: Session, id: int) -> model.BlogCategory | None:
    ret: Result = db.execute(
        select(model.BlogCategory).filter(model.BlogCategory.id == id)
    )
    return ret.scalars().first()

# 更新
def update_blog_category(db: Session, new_data: schema.BlogCategory, data: model.BlogCategory) -> model.BlogCategory:
    data.name = new_data.name
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# 削除
def delete_blog_category(db: Session, data: model.BlogCategory) -> None:
    db.delete(data)
    db.commit()
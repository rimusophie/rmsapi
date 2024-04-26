from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.engine import Result
from datetime import date

import api.models.blog as model
import api.models.blog_category as model_blog_category
import api.schemas.blog as schema

# 登録
def create_blog(db: Session, data: schema.BlogCreate) -> model.Blog:
    ret = model.Blog(**data.dict())
    db.add(ret)
    db.commit()
    db.refresh(ret)
    return ret

# 一覧取得
def get_blogs(db: Session) -> list[tuple[int, str, int, str, date]]:
    ret: Result = db.execute(
        select(
            model.Blog.id,
            model.Blog.title,
            model.Blog.blog_category_id,
            model_blog_category.BlogCategory.name,
            model.Blog.filename,
            model.Blog.updated_date
        ).outerjoin(model_blog_category.BlogCategory, model.Blog.blog_category_id == model_blog_category.BlogCategory.id)
    )
    return ret.all()

# 詳細取得
def get_blog(db: Session, id: int) -> model.Blog | None:
    ret: Result = db.execute(
        select(
            model.Blog
        ).outerjoin(
            model_blog_category.BlogCategory, model.Blog.blog_category_id == model_blog_category.BlogCategory.id
        ).filter(model.Blog.id == id)
    )
    return ret.scalars().first()

# 更新
def update_blog(db: Session, new_data: schema.Blog, data: model.Blog) -> model.Blog:
    data.title = new_data.title
    data.blog_category_id = new_data.blog_category_id
    data.filename = new_data.filename
    data.updated_date = new_data.updated_date
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

# 削除
def delete_blog(db: Session, data: model.Blog) -> None:
    db.delete(data)
    db.commit()
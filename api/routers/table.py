from fastapi import APIRouter, Depends

import api.cruds.table as crud
import api.schemas.table as schema
from api.db import get_engine

router = APIRouter()

# 一覧取得
@router.get("/tables", response_model = list[schema.Table])
def list_tables(engine = Depends(get_engine)):
    ret: list[schema.Table] = []

    # マッピングをしていないので手動で設定
    for tmp in crud.get_tables(engine):
        data = schema.Table(name = tmp)
        ret.append(data)
    
    engine.dispose()
    
    return ret

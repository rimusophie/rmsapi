from fastapi import APIRouter, Depends

import api.cruds.table as crud
import api.schemas.table as schema
from api.db import get_engine, get_env_info

router = APIRouter()

# テーブル一覧取得
@router.get("/tables", response_model = list[schema.Table])
def list_tables(engine = Depends(get_engine)):
    ret: list[schema.Table] = []

    # マッピングをしていないので手動で設定
    for tmp in crud.get_tables(engine):
        data = schema.Table(name = tmp)
        ret.append(data)
    
    engine.dispose()
    
    return ret

# DB情報取得
@router.get("/dbinfo", response_model = schema.DBInfo)
def detail_dbinfo(db_info = Depends(get_env_info)):
    # 環境ファイルから取得

    ret = schema.DBInfo(
        host = db_info["host"], 
        name = db_info["name"], 
        port = db_info["port"]
    )
    
    return ret

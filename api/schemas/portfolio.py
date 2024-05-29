from pydantic import BaseModel, Field, ConfigDict

# レスポンス
class PortfolioResponse(BaseModel):
    id: int
    name: str | None
    remark: str | None

    model_config = ConfigDict(from_attributes = True)

# リクエスト
class PortfolioRequest(BaseModel):
    name: str | None = Field(default = None, max_length = 200)
    remark: str | None = Field(default = None, max_length = 500)
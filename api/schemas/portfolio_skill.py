from pydantic import BaseModel, Field, ConfigDict

# レスポンス
class PortfolioSkillResponse(BaseModel):
    id: int
    portfolio_id: int | None
    skill_id: int | None

    model_config = ConfigDict(from_attributes = True)

# リクエスト
class PortfolioSkillRequest(BaseModel):
    portfolio_id: int | None = Field(default = None)
    skill_id: int | None = Field(default = None)
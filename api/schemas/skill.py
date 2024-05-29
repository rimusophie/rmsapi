from pydantic import BaseModel, Field, ConfigDict

# レスポンス
class SkillResponse(BaseModel):
    id: int
    name: str | None
    category: int | None

    model_config = ConfigDict(from_attributes = True)

# リクエスト
class SkillRequest(BaseModel):
    name: str | None = Field(default = None, max_length = 100)
    category: int | None = Field(default = None, ge = 0)
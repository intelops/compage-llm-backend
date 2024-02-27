import uuid

from pydantic import BaseModel, Field


class API_KEY_Schema(BaseModel):
    id: uuid = Field(default_factory=uuid.uuid4)
    username: str = Field(...)
    api_key: str = Field(...)

    class Config:
        schema_extra = {
            "example": {"username": "peter_parker", "api_key": "OPEN_AI_APIKEY"}
        }

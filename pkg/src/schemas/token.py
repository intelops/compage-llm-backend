from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenCreate(BaseModel):
    username: str
    api_key: str


class TokenPayload(BaseModel):
    sub: str

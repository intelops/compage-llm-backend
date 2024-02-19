from pydantic import BaseModel


class GPTRequest(BaseModel):
    prompt: str
    language: str


class GPTResponse(BaseModel):
    sub: str

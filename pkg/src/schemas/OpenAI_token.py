from pydantic import BaseModel


class openAI_API_KEY_request_schema(BaseModel):
    api_key: str
    username: str

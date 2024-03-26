"""
This module contains the GPTRequest and GPTResponse schemas for the GPT endpoint
"""

from pydantic import BaseModel
from fastapi import HTTPException


class GPTRequest(BaseModel):
    """
    GPTRequest schema for the request body of the GPT endpoint
    """

    prompt: str
    openai_api_key: str


class GPTResponse(BaseModel):
    """
    GPTResponse schema for the response body of the GPT endpoint
    """

    sub: str


class OpenAIRequest(BaseModel):
    """
    OpenAIRequest schema for the request body of the OpenAI endpoint
    """

    openai_api_key: str


def validate_gpt_request(request: GPTRequest):
    """
    Validates the GPTRequest object
    """

    if not request.prompt:
        raise HTTPException(status_code=400, detail="prompt cannot be empty")

    if not request.openai_api_key:
        raise HTTPException(status_code=400, detail="openai_api_key cannot be empty")

    return request

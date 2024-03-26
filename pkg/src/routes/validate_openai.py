from fastapi import APIRouter, HTTPException
from pkg.src.schemas.gpt import OpenAIRequest
import openai

router = APIRouter()


@router.post("/validate_openai")
async def validate_openai(request_body: OpenAIRequest):
    """
    A function to validate the OpenAI API key.
    """
    if not request_body.openai_api_key:
        raise HTTPException(status_code=400, detail="OpenAI API key is required")

    # Set the OpenAI API key
    openai.api_key = request_body.openai_api_key

    # Check if the API key is valid
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}]
        )
        return {
            "status": "success",
            "message": "API key is valid",
            "code": 200,
            "data": response.choices[0].message.content,
        }

    except openai.OpenAIError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

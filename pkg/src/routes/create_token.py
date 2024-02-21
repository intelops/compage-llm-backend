from datetime import timedelta
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

# internal
from pkg.src.constants.errors import INTERNAL_SERVER_ERROR
from pkg.src.models.openAI_Token import OpenAI_Token
from pkg.src.schemas.OpenAI_token import openAI_API_KEY_request_schema
from pkg.src.middleware.auth_handler import createJWT
from pkg.src.utils.openai_validator import openai_apikey_valid

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 7200


@router.post("/create-token")
async def create_token(openai_apikey_request: openAI_API_KEY_request_schema):
    """
    Function to create a token for the OpenAI API.

    Args:
        openai_apikey_request: Request schema containing the OpenAI API key and username.

    Returns:
        JSON response containing the access token and expires in time, or an error response.
    """

    # validation
    if openai_apikey_request.api_key == "" or openai_apikey_request.username == "":
        raise HTTPException(status_code=400, detail="Missing api_key or username")

    # openai_apikey validation
    try:
        openai_apikey_valid(openai_apikey_request.api_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    # main code starts here
    try:
        expires_delta = timedelta(minutes=24 * 60)  # Token expiration time
        token_data = {"sub": openai_apikey_request.username}
        access_token = createJWT(token_data, expires_delta)

        # check if user already exists
        query = OpenAI_Token.objects.filter(
            username=openai_apikey_request.username
        ).allow_filtering()

        if query.count() > 0:
            return {"access_token": access_token, "expires_in": expires_delta}

        # main gpt logic begins here
        os.environ["OPENAI_API_KEY"] = openai_apikey_request.api_key

        # store api_key in database
        result = OpenAI_Token.create_openai_apikey(
            api_key=openai_apikey_request.api_key,
            username=openai_apikey_request.username,
        )

        response = JSONResponse(
            content={"data": {"access_token": access_token, "data": result}}
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
        )

        # final response
        return response

    # exceptions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=INTERNAL_SERVER_ERROR,
            headers={"X-Error": str(e)},
        ) from e

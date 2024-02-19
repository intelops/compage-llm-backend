from pkg.src.schemas.token import TokenCreate
import uuid

api_key_store = []


def store_apikey(payload: TokenCreate):
    if payload.api_key == "" or payload.username == "":
        return None
    id = uuid.uuid4()
    result = {"id": id, "username": payload.username, "api_key": payload.api_key}
    api_key_store.append(result)
    return result


async def get_apikey(username: str):
    for key in api_key_store:
        if key["username"] == username:
            return key
    return None

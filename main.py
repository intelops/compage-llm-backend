from contextlib import asynccontextmanager

import uvicorn

# cassandra connection
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI

from logger import logger
from pkg.src.config.database import get_session
from pkg.src.middleware.cors import cors_middleware
from pkg.src.models.openAI_Token import OpenAI_Token

# inbuilt packages
from pkg.src.routes import create_token, gpt, health

DB_SESSION = ""


@asynccontextmanager
async def lifespan(application: FastAPI):
    # trigger everytime the app starts
    global DB_SESSION
    DB_SESSION = get_session()
    sync_table(OpenAI_Token)
    logger.info("Database connected!")
    yield


app = FastAPI(lifespan=lifespan)


# cors middleware
cors_middleware(app)

# routes
app.include_router(health.router, tags=["Health"], prefix="/api")
app.include_router(create_token.router, tags=["Auth"], prefix="/api")
app.include_router(gpt.router, tags=["GPT"], prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

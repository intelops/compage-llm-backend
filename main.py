from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from logger import logger
from pkg.src.config.database import get_session
from pkg.src.middleware.cors import cors_middleware

# inbuilt packages
from pkg.src.routes import health, unit_test, doc_generation, validate_openai


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    # trigger everytime the app starts
    """
    db_session = get_session()
    if not db_session:
        logger.error("Database connection failed!")
        return
    logger.info("Database connected!")
    yield


app = FastAPI(lifespan=lifespan)

# cors middleware
cors_middleware(app)

# routes
app.include_router(health.router, tags=["Health"], prefix="/api")
app.include_router(validate_openai.router, tags=["OpenAI Validation"], prefix="/api")
app.include_router(unit_test.router, tags=["Unit Test Generation"], prefix="/api")
app.include_router(
    doc_generation.router, tags=["Documentation Generation"], prefix="/api"
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

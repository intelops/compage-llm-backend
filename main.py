import uvicorn
from fastapi import FastAPI

# inbuilt packages
from pkg.src.routes import gpt, health, create_token
from pkg.src.middleware.cors import cors_middleware
from pkg.src.config.database import get_session
from pkg.src.models.openAI_Token import OpenAI_Token

# cassandra connection
from cassandra.cqlengine.management import sync_table


app = FastAPI()


@app.on_event("startup")
def startup_event():
    # trigger everytime the app starts
    global DB_SESSION
    DB_SESSION = get_session()
    sync_table(OpenAI_Token)
    print("Database connected!")


# cors middleware
cors_middleware(app)

# routes
app.include_router(health.router, tags=["Health"], prefix="/api")
app.include_router(create_token.router, tags=["Auth"], prefix="/api")
app.include_router(gpt.router, tags=["GPT"], prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

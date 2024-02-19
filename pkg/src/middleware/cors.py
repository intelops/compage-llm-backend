from fastapi.middleware.cors import CORSMiddleware


# This is a cors middleware for the entire app
# make sure to change the origins accordingly
def cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

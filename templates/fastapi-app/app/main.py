from fastapi import FastAPI

from app.config import settings
from app.database.session import database
from app.routes import health_check, v1


app = FastAPI(
    title="<REPO_NAME>",
    description="<REPO_DESCRIPTION>",
    version=settings.release_version,
)


@app.on_event("startup")
async def startup():
    # Add repo specific start up commands here
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # Add repo specific shutdown commands here
    await database.disconnect()


app.include_router(health_check.router, tags=["health"])
app.include_router(v1.router, prefix="/v1", tags=["API v1"])

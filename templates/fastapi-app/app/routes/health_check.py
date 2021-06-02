import time
import logging
from fastapi import APIRouter
from starlette.responses import Response

from starlette import status

from app.database.session import database
from app.schemas.response_models import Health, StatusEnum


router = APIRouter()
logger = logging.getLogger(__name__)


async def db_health(response: Response, name: str):
    try:
        start: float = time.perf_counter()
        await database.execute("SELECT 1")
        elapsed_time: float = time.perf_counter() - start

        if elapsed_time > 1:
            logger.info(
                "%s health check took longer than 1 second: %s",
                name,
                elapsed_time,
            )

        return {"status": StatusEnum.STATUS_UP}

    except Exception as exception:
        logger.warning("%s health check failed", name, exc_info=True)
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return {"status": StatusEnum.STATUS_DOWN, "error": str(exception)}


@router.get(
    "/health-check/",
    summary="Service health check.",
    response_description="Service health status",
    response_model=Health,
)
async def health(response: Response):
    """
    Returns a health check for this service and its dependencies.
    """

    db = await db_health(response, "<REPO_NAME> Database")
    return {
        "service": {"status": StatusEnum.STATUS_UP},
        "database": db,
    }

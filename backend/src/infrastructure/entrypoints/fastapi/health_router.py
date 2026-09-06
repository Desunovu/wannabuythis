from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from sqlalchemy import Engine, text
from starlette import status
from starlette.responses import JSONResponse

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("/live")
async def liveness():
    """Application is alive."""
    return {"status": "alive"}


@health_router.get("/ready")
@inject
async def readiness(engine: FromDishka[Engine]):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return {"status": "ready"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready"},
        )

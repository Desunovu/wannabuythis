from sqlalchemy import text
from src.infrastructure.database.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from starlette import status
from starlette.responses import JSONResponse

from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("/live")
async def liveness():
    """Application is alive."""
    return {"statis": "alive"}


@health_router.get("/ready")
async def readiness():
    """Application is ready to serve requests."""
    try:
        engine = SQLAlchemyUnitOfWork.get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return {"status": "ready"}
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready"},
        )

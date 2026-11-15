import logging

from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.shared.application.exceptions import (
    ConflictException,
    Forbidden,
    NotFoundException,
    TokenException,
    ValidationException,
    VerificationException,
)

logger = logging.getLogger(__name__)

INTEGRITY_ERROR_DETAIL = "Data conflict"


def _detail_handler(status_code: int):
    def handler(request: Request, exception: Exception) -> JSONResponse:
        detail = exception.args[0] if exception.args else str(exception)
        return JSONResponse(status_code=status_code, content={"detail": detail})

    return handler


def handle_sqlalchemy_integrity_error(
    request: Request, exception: IntegrityError
) -> JSONResponse:
    logger.warning(f"IntegrityError: {exception.orig.args[0]}")
    return JSONResponse(
        status_code=HTTP_409_CONFLICT, content={"detail": INTEGRITY_ERROR_DETAIL}
    )


exception_to_exception_handlers = {
    NotFoundException: _detail_handler(HTTP_404_NOT_FOUND),
    ConflictException: _detail_handler(HTTP_409_CONFLICT),
    ValidationException: _detail_handler(HTTP_422_UNPROCESSABLE_ENTITY),
    VerificationException: _detail_handler(HTTP_401_UNAUTHORIZED),
    Forbidden: _detail_handler(HTTP_403_FORBIDDEN),
    TokenException: _detail_handler(HTTP_401_UNAUTHORIZED),
    IntegrityError: handle_sqlalchemy_integrity_error,
}

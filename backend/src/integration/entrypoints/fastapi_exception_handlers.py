from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from src.common.service.exceptions import (
    ConflictException,
    Forbidden,
    NotFoundException,
    TokenException,
    VerificationException,
    ValidationException,
)


def handle_not_found(request: Request, exception: NotFoundException):
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=exception.args[0])


def handle_conflict(request: Request, exception: ConflictException):
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail=exception.args[0])


def handle_validation_error(request: Request, exception: ValidationException):
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail=exception.args[0])


def handle_verification_error(request: Request, exception: VerificationException):
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=exception.args[0])


def handle_forbidden(request: Request, exception: Forbidden):
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=exception.args[0])


def handle_token_error(request: Request, exception: TokenException):
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=exception.args[0])


def handle_sqlalchemy_integrity_error(request: Request, exception: IntegrityError):
    raise HTTPException(status_code=HTTP_409_CONFLICT, detail=exception.orig.args[0])


exception_to_exception_handlers = {
    NotFoundException: handle_not_found,
    ConflictException: handle_conflict,
    ValidationException: handle_validation_error,
    VerificationException: handle_verification_error,
    Forbidden: handle_forbidden,
    IntegrityError: handle_sqlalchemy_integrity_error,
}

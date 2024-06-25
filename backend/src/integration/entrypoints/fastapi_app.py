from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src import bootstrap, config
from src.common.dependencies.notificator import EmailNotificator
from src.common.dependencies.password_hash_util import HashlibPasswordHashUtil
from src.common.dependencies.token_manager import JWTManager
from src.common.dependencies.uuid_generator import DefaultUUIDGenerator
from src.common.entrypoints.fastapi_limiter import limiter
from src.integration.adapters.sqlalchemy_orm import start_sqlalchemy_mappers
from src.integration.entrypoints.fastapi_exception_handlers import (
    exception_to_exception_handlers,
)
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.users.entrypoints.fastapi.admin_router import users_admin_router
from src.users.entrypoints.fastapi.auth_router import users_auth_router
from src.users.entrypoints.fastapi.command_router import users_command_router
from src.users.entrypoints.fastapi.query_router import users_query_router
from tests.conftest import FakeNotificator


def create_app():
    app = FastAPI(lifespan=lifespan)

    app.include_router(users_auth_router)
    app.include_router(users_query_router)
    app.include_router(users_command_router)
    app.include_router(users_admin_router)

    for exception, exception_handler in exception_to_exception_handlers.items():
        app.add_exception_handler(
            exc_class_or_status_code=exception, handler=exception_handler
        )

    return app


@asynccontextmanager
async def lifespan(application: FastAPI):
    start_sqlalchemy_mappers()

    dependencies = setup_dependencies_for_environment()
    messagebus = bootstrap.initialize_messagebus(dependencies=dependencies)

    # Save objects in app state
    application.state.limiter = limiter
    application.state.dependencies = dependencies
    application.state.messagebus = messagebus

    yield


def setup_dependencies_for_environment():
    """Set up dependencies for app environment"""

    notificator = (
        FakeNotificator() if config.get_env() == "development" else EmailNotificator()
    )

    dependencies = bootstrap.initialize_dependencies(
        uow=SQLAlchemyUnitOfWork(),
        password_hash_util=HashlibPasswordHashUtil(),
        uuid_generator=DefaultUUIDGenerator(),
        token_manager=JWTManager(),
        notificator=notificator,
    )
    return dependencies


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

from contextlib import asynccontextmanager

import uvicorn
from fakeredis import FakeRedis
from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers
from fastapi.middleware.cors import CORSMiddleware

from src import bootstrap, config
from src.common.utils.activation_code_generator import (
    RandomActivationCodeGenerator,
)
from src.common.utils.notificator import EmailNotificator
from src.common.utils.password_manager import HashlibPasswordManager
from src.common.utils.token_manager import JWTManager
from src.common.utils.uuid_generator import DefaultUUIDGenerator
from src.common.entrypoints.fastapi_limiter import limiter
from src.integration.adapters.alembic_runner import run_migrations
from src.integration.adapters.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)
from src.integration.adapters.sqlalchemy_orm import start_sqlalchemy_mappers
from src.integration.entrypoints.fastapi_exception_handlers import (
    exception_to_exception_handlers,
)
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.users.entrypoints.fastapi.admin_router import users_admin_router
from src.users.entrypoints.fastapi.auth_router import users_auth_router
from src.users.entrypoints.fastapi.command_router import users_command_router
from src.users.entrypoints.fastapi.query_router import users_query_router
from src.wishlists.entrypoints.fastapi.command_router import wishlists_command_router
from src.wishlists.entrypoints.fastapi.query_router import wishlists_query_router
from tests.fakes import FakeNotificator

ROUTERS = [
    users_admin_router,
    users_auth_router,
    users_query_router,
    users_command_router,
    wishlists_query_router,
    wishlists_command_router,
]


@asynccontextmanager
async def lifespan(application: FastAPI):
    start_sqlalchemy_mappers()
    if config.get_env() != "test":
        run_migrations()
    yield
    clear_mappers()


def setup_messagebus_dependencies():
    """Set up utils for messagebus based on app environment"""

    notificator = (
        FakeNotificator() if config.get_env() == "development" else EmailNotificator()
    )
    redis_client = FakeRedis() if config.get_env() == "development" else None

    dependencies = bootstrap.create_dependencies_dict(
        uow=SQLAlchemyUnitOfWork(),
        password_manager=HashlibPasswordManager(),
        uuid_generator=DefaultUUIDGenerator(),
        activation_code_generator=RandomActivationCodeGenerator(),
        activation_code_storage=RedisActivationCodeStorage(redis_client=redis_client),
        token_manager=JWTManager(),
        notificator=notificator,
    )
    return dependencies


def create_app():
    app = FastAPI(lifespan=lifespan)

    # Set up CORS
    origins = [
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize utils and messagebus
    dependencies = setup_messagebus_dependencies()
    messagebus = bootstrap.initialize_messagebus(dependencies=dependencies)

    # Save objects in app state
    app.state.limiter = limiter
    app.state.dependencies = dependencies
    app.state.messagebus = messagebus

    # Include routers
    for router in ROUTERS:
        app.include_router(router)

    # Register exception handlers
    for exception, exception_handler in exception_to_exception_handlers.items():
        app.add_exception_handler(
            exc_class_or_status_code=exception, handler=exception_handler
        )

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

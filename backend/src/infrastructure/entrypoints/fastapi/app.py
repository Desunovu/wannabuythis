import logging
from contextlib import asynccontextmanager

import uvicorn
from fakeredis import FakeRedis
from sqlalchemy.orm import clear_mappers
from src import bootstrap
from src.config import settings
from src.infrastructure.cache.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)
from src.infrastructure.database.sqlalchemy.database_manager import (
    run_migrations,
    wait_for_database,
)
from src.infrastructure.database.sqlalchemy.orm import start_sqlalchemy_mappers
from src.infrastructure.database.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from src.infrastructure.entrypoints.fastapi.exception_handlers import (
    exception_to_exception_handlers,
)
from src.infrastructure.entrypoints.fastapi.health_router import health_router
from src.infrastructure.entrypoints.fastapi.limiter import limiter
from src.modules.users.entrypoints.fastapi.admin_router import users_admin_router
from src.modules.users.entrypoints.fastapi.auth_router import users_auth_router
from src.modules.users.entrypoints.fastapi.command_router import users_command_router
from src.modules.users.entrypoints.fastapi.query_router import users_query_router
from src.modules.wishlists.entrypoints.fastapi.command_router import (
    wishlists_command_router,
)
from src.modules.wishlists.entrypoints.fastapi.query_router import (
    wishlists_query_router,
)
from src.shared.utils.activation_codes.activation_code_generator import (
    RandomActivationCodeGenerator,
)
from src.shared.utils.auth.password_manager import HashlibPasswordManager
from src.shared.utils.auth.token_manager import JWTManager
from src.shared.utils.generators.uuid_generator import DefaultUUIDGenerator
from src.shared.utils.notifications.notificator import EmailNotificator
from tests.fakes import FakeNotificator

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

ROUTERS = [
    users_admin_router,
    users_auth_router,
    users_query_router,
    users_command_router,
    wishlists_query_router,
    wishlists_command_router,
    health_router,
]

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Starting FastAPI application")

    # Setup ORM
    start_sqlalchemy_mappers()

    # Initialize database (skip in tests)
    if not settings.is_testing:
        wait_for_database()
        run_migrations()

    logger.info("FastAPI application started")

    yield

    # Cleanup
    logger.info("Shutting down FastAPI application")
    clear_mappers()


def setup_messagebus_dependencies():
    """Set up utils for messagebus based on app environment"""

    notificator = FakeNotificator() if settings.is_development else EmailNotificator()
    redis_client = FakeRedis() if settings.is_development else None

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


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function names.
    Should be called only afterr all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            parts = [str(t) for t in route.tags] + [route.name]
            route.operation_id = "_".join(parts)


def create_app():
    app = FastAPI(lifespan=lifespan)

    # Set up CORS
    origins = [
        "http://localhost",
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

    # Simplify generated IDs
    use_route_names_as_operation_ids(app)

    # Register exception handlers
    for exception, exception_handler in exception_to_exception_handlers.items():
        app.add_exception_handler(
            exc_class_or_status_code=exception, handler=exception_handler
        )

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

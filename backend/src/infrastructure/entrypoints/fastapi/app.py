import logging
from contextlib import asynccontextmanager

import uvicorn
from dishka import Container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from sqlalchemy import Engine
from sqlalchemy.orm import clear_mappers

from src.config import settings
from src.infrastructure.database.sqlalchemy.database_manager import (
    run_migrations,
    wait_for_database,
)
from src.infrastructure.database.sqlalchemy.orm import start_sqlalchemy_mappers
from src.infrastructure.di.container import (
    create_development_container,
    create_production_container,
)
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
    # Prepare database (skip in tests)
    if not settings.is_testing:
        container: Container = application.state.dishka_container
        engine = container.get(Engine)
        wait_for_database(engine)
        run_migrations()

    logger.info("FastAPI application started")
    yield

    logger.info("Shutting down FastAPI application")
    clear_mappers()


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function names.
    Should be called only afterr all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            parts = [str(t) for t in route.tags] + [route.name]
            route.operation_id = "_".join(parts)


def create_app(container: Container | None = None):
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

    # Init dishka container
    if container is None:
        container = (
            create_production_container()
            if settings.is_production
            else create_development_container()
        )
    setup_dishka(container, app)

    # Save objects in app state
    app.state.limiter = limiter

    # Include routers
    for router in ROUTERS:
        app.include_router(router)

    # Simplify generated IDs
    use_route_names_as_operation_ids(app)

    # Register exception handlers
    for exc, handler in exception_to_exception_handlers.items():
        app.add_exception_handler(exc_class_or_status_code=exc, handler=handler)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

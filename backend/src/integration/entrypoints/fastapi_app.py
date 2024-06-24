from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src import bootstrap, config
from src.common.adapters.dependencies import (
    FakeNotificator,
    EmailNotificator,
    HashlibPasswordHashUtil,
    DefaultUUIDGenerator,
    JWTManager,
)
from src.common.entrypoints.fastapi_limiter import limiter
from src.integration.adapters.sqlalchemy_orm import start_mappers
from src.integration.entrypoints.fastapi_exception_handlers import (
    exception_to_exception_handlers,
)
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.users.entrypoints.fastapi_admin_user_command_router import (
    admin_user_command_router,
)
from src.users.entrypoints.fastapi_auth_router import auth_router
from src.users.entrypoints.fastapi_users_command_router import users_command_router
from src.users.entrypoints.fastapi_users_query_router import users_query_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    start_mappers()

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


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(users_query_router)
app.include_router(users_command_router)
app.include_router(admin_user_command_router)

for exception, exception_handler in exception_to_exception_handlers.items():
    app.add_exception_handler(
        exc_class_or_status_code=exception, handler=exception_handler
    )


@app.get("/")
async def root():
    return {"message": "This is the WannaBuyThis REST API."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

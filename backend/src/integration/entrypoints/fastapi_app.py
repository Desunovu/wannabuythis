from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src import bootstrap, config
from src.common.adapters.dependencies import FakeNotificator, EmailNotificator
from src.common.entrypoints.fastapi_limiter import limiter
from src.integration.adapters.sqlalchemy_orm import start_mappers
from src.users.entrypoints.fastapi_auth_router import auth_router
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
    notificator = EmailNotificator()
    if config.get_env() == "development":
        notificator = FakeNotificator()

    dependencies = bootstrap.initialize_dependencies(notificator=notificator)
    return dependencies


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "This is the WannaBuyThis REST API."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

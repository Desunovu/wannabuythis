from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src import bootstrap, config
from src.common.adapters.dependencies import FakeNotificator, EmailNotificator
from src.common.entrypoints.fastapi_limiter import limiter
from src.integration.adapters.sqlalchemy_orm import start_mappers
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.users.entrypoints.fastapi_auth_router import auth_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Set up SQLAlchemy ORM
    start_mappers()

    # Set up rate limiter
    application.state.limiter = limiter

    # Set up dependencies for app environment
    notificator = EmailNotificator()
    if config.get_env() == "development":
        notificator = FakeNotificator()

    # Set up messagebus
    application.state.messagebus = bootstrap.bootstrap(
        uow=SQLAlchemyUnitOfWork(), notificator=notificator
    )
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "This is the WannaBuyThis REST API."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

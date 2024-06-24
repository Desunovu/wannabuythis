from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import bootstrap
from src.integration.adapters.sqlalchemy_orm import start_mappers
from src.integration.service.sqlalchemy_uow import SQLAlchemyUnitOfWork
from src.users.entrypoints.fastapi_auth_router import auth_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    start_mappers()
    application.state.messagebus = bootstrap.bootstrap(uow=SQLAlchemyUnitOfWork())
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "This is the WannaBuyThis REST API."}

"""Приложение FastApi."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from fastapi_app.configs import async_engine, settings
from fastapi_app.exceptions import register_exception_handler
from fastapi_app.routes import (
    account_rout,
    admin_dist_rout,
    auth_rout,
    jwt_rout,
    pay_rout,
)


@asynccontextmanager
async def database_life_cycle(app: FastAPI) -> AsyncIterator:
    """
    Асинхронное соединение с базой движка.

    Устанавливает и закрывает соединение.
    """
    yield
    await async_engine.dispose()


app_ = FastAPI(
    lifespan=database_life_cycle,
    default_response_class=ORJSONResponse,
)

register_exception_handler(app_)

app_.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,  # разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # разрешённые HTTP методы
    # allow_headers=["*"],
    allow_headers=["Content-Type", "X-My-Fancy-Header"],
    expose_headers=["Content-Type", "X-Custom-Header"],
)

app_.include_router(jwt_rout, prefix=settings.app.api_prefix)
app_.include_router(admin_dist_rout, prefix=settings.app.api_prefix)
app_.include_router(auth_rout, prefix=settings.app.api_prefix)
app_.include_router(account_rout, prefix=settings.app.api_prefix)
app_.include_router(pay_rout, prefix=settings.app.api_prefix)

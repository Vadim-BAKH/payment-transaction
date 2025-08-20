"""Модуль конфигурации зависимости от генератора синхронной сессии."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.database import get_session_db

DBSessionDep = Annotated[
    AsyncSession,
    Depends(get_session_db),
]

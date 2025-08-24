"""Конфигуратор тестов."""

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.app import app_
from fastapi_app.configs import (
    async_test_engine,
    async_test_session,
)
from fastapi_app.database import get_session_db
from fastapi_app.models import Base


@pytest.fixture(autouse=True)
async def override_dependencies():
    """Переопределяет основную сессию на тестовую."""

    async def override_get_db() -> AsyncGenerator[
        AsyncSession,
        None,
    ]:
        """Создает сессию для тестов."""
        async with async_test_session() as session:
            yield session

    app_.dependency_overrides[get_session_db] = override_get_db
    yield
    app_.dependency_overrides.clear()


@pytest.fixture
async def db_session() -> AsyncGenerator[
    AsyncSession,
    None,
]:
    """Возвращает тестовую сессию базы данных."""
    async with async_test_session() as session:
        yield session


@pytest.fixture(autouse=True)
async def test_database() -> AsyncGenerator:
    """Фикстура для управления миграциями."""
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield

    finally:
        async with async_test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await async_test_engine.dispose()


@pytest.fixture
async def client():
    """Возвращает асинхронный клиент."""
    async with AsyncClient(
        transport=ASGITransport(app=app_),
        base_url="http://test",
    ) as ac:
        yield ac

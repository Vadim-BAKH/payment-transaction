"""Конфигуратор тестов."""

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi_app.app import app_
from fastapi_app.configs import (
    async_test_engine,
    async_test_session,
    settings,
)
from fastapi_app.database import get_session_db
from fastapi_app.models import Base
from fastapi_app.repositories import AccountRepo, PaymentRepo, UserRepo
from fastapi_app.schemas import CreatePayment, UserCreate
from fastapi_app.services import PaymentService, UserService


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


@pytest.fixture
async def user_account(db_session):
    """Создаёт тестового пользователя в тестовой базе через сервис UserService."""
    user_repo = UserRepo(session=db_session)
    user_service = UserService(user_repo=user_repo)

    user_in = UserCreate(
        email=settings.test_user.email,
        password=settings.test_user.password,
        password_confirm=settings.test_user.password,
        first_name=settings.test_user.first_name,
        last_name=settings.test_user.last_name,
    )

    user = await user_service.register_user(user_in)
    await db_session.commit()
    yield user


@pytest.fixture
async def payment_fixture(
    db_session: AsyncSession,
    user_account,
) -> AsyncGenerator:
    """
    Фикстура для создания тестового платежа и счета для пользователя.

    Использует PaymentService, создаёт:
      - счет для пользователя (если отсутствует),
      - платеж с уникальным transaction_id.
    """
    # Репозитории и сервис
    account_repo = AccountRepo(session=db_session)
    payment_repo = PaymentRepo(session=db_session)
    payment_service = PaymentService(
        account_repo=account_repo,
        payment_repo=payment_repo,
    )

    # Создаем платеж
    payment_in = CreatePayment(
        user_id=user_account.id,
        account_id=1,
        amount=1000,
    )
    payment_out = await payment_service.create_payment_and_update_balance(
        payment_in,
    )

    await db_session.commit()

    yield {
        "payment": payment_out,
        "service": payment_service,
    }


@pytest.fixture
async def auth_token(client: AsyncClient, user_account) -> str:
    """Фикстура для получения JWT access_token тестового пользователя."""
    response = await client.post(
        "/api/jwt/login",
        data={
            "username": settings.test_user.email,
            "password": settings.test_user.password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()["access_token"]

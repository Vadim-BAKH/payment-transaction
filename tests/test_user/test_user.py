"""Тесты авторизации и получения информации о текущем пользователе."""

import pytest
from fastapi import status
from httpx import AsyncClient

from fastapi_app.configs import settings


@pytest.mark.asyncio
@pytest.mark.user
async def test_login_and_get_me(client: AsyncClient, auth_token):
    """Проверяет получение данных текущего пользователя после авторизации."""
    # Получение текущего пользователя
    response = await client.get(
        "/api/auth/users/me",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK

    user_data = response.json()
    assert user_data["first_name"] == settings.test_user.first_name
    assert user_data["email"] == settings.test_user.email

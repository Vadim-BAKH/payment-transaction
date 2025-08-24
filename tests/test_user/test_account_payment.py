"""Тесты функционала платежей и балансов пользователя."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.user
async def test_get_accounts_payments(
    client: AsyncClient,
    auth_token,
    payment_fixture,
):
    """Проверяет корректное получение баланса и платежей пользователя."""
    # Получение баланса
    response = await client.get(
        "/api/accounts/look",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    accounts = response.json()["accounts"]
    assert len(accounts) > 0
    assert accounts[0]["balance"] == 1000

    # Получение платежей
    response = await client.get(
        "/api/payments/look",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    payments = response.json()["payments"]
    assert len(payments) > 0
    assert payments[0]["transaction_id"]
    assert payments[0]["amount"] == 1000

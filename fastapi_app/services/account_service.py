"""Модуль сервиса работы со счетами пользователя."""

from typing import Sequence

from fastapi_app.exceptions import AccountNotFound
from fastapi_app.models import Account
from fastapi_app.repositories import AccountRepo
from fastapi_app.schemas import AccountCreate, AccountOut, AccountsList


class AccountService:
    """Сервис для управления логикой балансовых счетов."""

    def __init__(self, account_repo: AccountRepo):
        """Инициализация с репозиторием счетов."""
        self.account_repo = account_repo

    async def get_all_user_accounts(self, user_id: int) -> AccountsList:
        """Получение всех активных счетов пользователя."""
        accounts: Sequence[Account] = await self.account_repo.get_all_accounts(
            user_id=user_id,
        )
        if not accounts:
            raise AccountNotFound()
        accounts_out = [
            AccountOut.model_validate(
                account,
            )
            for account in accounts
        ]
        return AccountsList(accounts=accounts_out)

    async def create_user_account(self, user_in: AccountCreate) -> Account:
        """Создание счёта пользователя."""
        account = await self.account_repo.create_account(
            user_id=user_in.user_id,
        )
        return account

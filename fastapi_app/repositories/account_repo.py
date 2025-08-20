"""Репозиторий для работы со счётом в базе данных."""

from typing import Optional

from sqlalchemy import Sequence, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.models import Account


class AccountRepo:
    """Репозиторий для CRUD операций с балансовым счётом."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация сессии базы данных."""
        self.session = session

    async def get_all_accounts(self, user_id: int) -> Sequence[Account]:
        """Получить все счета пользователя."""
        stmt = select(Account).where(
            Account.user_id == user_id,
            Account.is_active,
        )
        result = await self.session.execute(stmt)
        accounts_orm = result.scalars().all()
        return accounts_orm

    async def get_account_by_id(self, account_id: int) -> Account | None:
        """Получает платежный счёт по id."""
        stmt = select(Account).where(
            Account.id == account_id,
            Account.is_active,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_account(self, user_id: int) -> Account:
        """Создать новый счёт для пользователя."""
        account = Account(user_id=user_id)
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def update_balance(
        self,
        account_id: int,
        amount: float,
    ) -> Optional[Account]:
        """Обновить баланс счета, увеличив его на amount."""
        stmt = (
            update(Account)
            .where(
                Account.id == account_id,
                Account.is_active,
            )
            .values(balance=Account.balance + amount)
            .returning(Account)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        updated_account = result.scalar_one_or_none()
        return updated_account

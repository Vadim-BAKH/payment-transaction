"""Репозиторий для работы со счётом в базе данных."""

from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.models import Account


class AccountRepo:
    """Репозиторий для CRUD операций с балансовым счётом."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация сессии базы данных."""
        self.session = session

    async def get_all_accounts(self, user_id: int) -> Sequence[Account]:
        """Получить все счета пользователя."""
        smtp = select(Account).where(
            Account.user_id == user_id,
            Account.is_active,
        )
        result = await self.session.execute(smtp)
        accounts_orm = result.scalars().all()
        return accounts_orm

    async def create_account(self, user_id: int) -> Account:
        """Создать новый счёт для пользователя."""
        account = Account(user_id=user_id)
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

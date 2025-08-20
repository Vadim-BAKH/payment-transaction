"""Репозиторий для получения общей информации."""

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi_app.models import User


class AllUserInfo:
    """Репозиторий для получения необходимой информации."""

    def __init__(self, session: AsyncSession):
        """Инициализация сессии базы данных."""
        self.session = session

    async def get_users_balance_position(self, params: Params):
        """Получить всех пользователей с их счетами и балансами."""
        stmt = select(User).options(joinedload(User.accounts))
        return await paginate(self.session, stmt, params)

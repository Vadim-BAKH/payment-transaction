"""Модуль сервиса получения полной информации."""

from fastapi_pagination import Params

from fastapi_app.repositories import AllUserInfo
from fastapi_app.schemas import ListAllUserInfoOut


class UserService:
    """Сервис для управления логикой пользователей."""

    def __init__(self, info_repo: AllUserInfo):
        """Инициализация с репозиторием получения информации."""
        self.info_repo = info_repo

    async def get_all_users_info(self, params: Params) -> ListAllUserInfoOut:
        """
        Получить всех пользователей с их счетами и балансами.

        :param: Параметры пагинации (номер страницы, размер страницы)
        :return: пагинированный список пользователей с их счетами.
        """
        users_info = await self.info_repo.get_users_balance_position(params)
        return ListAllUserInfoOut(info=users_info)

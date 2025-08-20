"""Модуль возвращает экземпляр репозитория для пользователя."""

from fastapi_app.dependencies.db_session import DBSessionDep
from fastapi_app.repositories import UserRepo


def get_user_repo(session: DBSessionDep) -> UserRepo:
    """
    Зависимость получения репозитория пользователей.

    :param session: Сессия базы данных
    :return: Экземпляр UserRepo
    """
    return UserRepo(session=session)

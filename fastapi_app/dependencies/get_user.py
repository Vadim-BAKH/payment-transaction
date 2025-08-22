"""Модуль возвращает экземпляр репозитория для пользователя."""

from fastapi import Depends

from fastapi_app.dependencies.db_session import DBSessionDep
from fastapi_app.repositories import UserRepo
from fastapi_app.services import UserService


def get_user_repo(session: DBSessionDep) -> UserRepo:
    """
    Зависимость получения репозитория пользователей.

    :param session: Сессия базы данных
    :return: Экземпляр UserRepo
    """
    return UserRepo(session=session)


async def get_user_service(
    repo: UserRepo = Depends(get_user_repo),
) -> UserService:
    """
    Зависимость получения сервиса пользователя.

    :param repo: Экземпляр UserRepo.
    :return: Экземпляр UserService.
    """
    return UserService(user_repo=repo)

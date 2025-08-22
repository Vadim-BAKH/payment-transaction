"""Модуль возвращает экземпляры репозитория и сервиса для счёта."""

from fastapi import Depends

from fastapi_app.dependencies.db_session import DBSessionDep
from fastapi_app.repositories import AccountRepo
from fastapi_app.services import AccountService


def get_account_repo(session: DBSessionDep) -> AccountRepo:
    """
    Зависимость получения репозитория Счета.

    :param session: Сессия базы данных
    :return: Экземпляр AccountRepo
    """
    return AccountRepo(session=session)


async def get_account_service(
    repo: AccountRepo = Depends(get_account_repo),
) -> AccountService:
    """
    Зависимость получения сервиса Счёта.

    :param repo: Экземпляр AccountRepo.
    :return: Экземпляр AccountService.
    """
    return AccountService(account_repo=repo)

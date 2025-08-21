"""Модуль возвращает экземпляры репозитория и сервиса для информации."""

from fastapi import Depends

from fastapi_app.dependencies.db_session import DBSessionDep
from fastapi_app.repositories import AllUserInfoRepo
from fastapi_app.services import AllUserInfoService


def get_info_repo(session: DBSessionDep) -> AllUserInfoRepo:
    """
    Зависимость получения репозитория Информации о пользователях и счетах..

    :param session: Сессия базы данных
    :return: Экземпляр AllUserInfoRepo
    """
    return AllUserInfoRepo(session=session)


async def get_info_users_accounts_service(
    repo: AllUserInfoRepo = Depends(get_info_repo),
) -> AllUserInfoService:
    """
    Зависимость получения сервиса Информации о пользователях.

    :param repo: Экземпляр AllUserInfoRepo.
    :return: Экземпляр AllUserInfoService.
    """
    return AllUserInfoService(info_repo=repo)

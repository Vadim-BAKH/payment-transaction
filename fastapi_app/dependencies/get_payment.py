"""Модуль возвращает экземпляры репозитория и сервиса для счёта."""

from fastapi import Depends

from fastapi_app.dependencies.db_session import DBSessionDep
from fastapi_app.dependencies.get_account import get_account_repo
from fastapi_app.repositories import AccountRepo, PaymentRepo
from fastapi_app.services import PaymentService


def get_payment_repo(session: DBSessionDep) -> PaymentRepo:
    """
    Зависимость получения репозитория транзакции.

    :param session: Сессия базы данных
    :return: Экземпляр PaymentRepo
    """
    return PaymentRepo(session=session)


async def get_payment_service(
    payment_repo: PaymentRepo = Depends(get_payment_repo),
    account_repo: AccountRepo = Depends(get_account_repo),
) -> PaymentService:
    """
    Создает и возвращает сервис для работы с платежами.

    :param payment_repo: Репозиторий платежей
    :param account_repo: Репозиторий счетов
    :return: Экземпляр PaymentService
    """
    return PaymentService(
        account_repo=account_repo,
        payment_repo=payment_repo,
    )

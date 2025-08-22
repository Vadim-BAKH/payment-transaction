"""Модель сервисов транзакций."""

from typing import Sequence

from fastapi_app.exceptions import (
    PaymentNotFound,
    TransactionAlreadyProcessed,
)
from fastapi_app.models import Payment
from fastapi_app.repositories import AccountRepo, PaymentRepo
from fastapi_app.schemas import (
    CreatePayment,
    PaymentOut,
    PaymentsList,
)


class PaymentService:
    """Сервис для управления платежами и балансами счетов."""

    def __init__(
        self,
        account_repo: AccountRepo,
        payment_repo: PaymentRepo,
    ):
        """Инициализация с репозиториями счетов и платежей."""
        self.account_repo = account_repo
        self.payment_repo = payment_repo

    async def check_unique_transaction_id(self, data: CreatePayment) -> bool:
        """Проверяет уникальность transaction_id."""
        existing = await self.payment_repo.get_by_transaction_id(
            transaction_id=data.transaction_id,
        )
        if existing:
            raise TransactionAlreadyProcessed()
        return False

    async def create_payment_and_update_balance(
        self,
        payment_in: CreatePayment,
    ) -> PaymentOut:
        """
        Создать платеж и обновить баланс счета.

        Если счет с указанным account_id отсутствует, создает новый счет
        с балансом, равным сумме платежа. Если счет существует, увеличивает
        его баланс на сумму платежа.

        :param payment_in: Данные нового платежа.
        :return: Объект созданного платежа.
        """
        await self.check_unique_transaction_id(data=payment_in)
        account = await self.account_repo.get_account_by_id(
            account_id=payment_in.account_id,
        )
        if not account:
            account = await self.account_repo.create_account(
                user_id=payment_in.user_id,
            )
        payment = await self.payment_repo.create_payment(
            transaction_id=payment_in.transaction_id,
            account_id=account.id,
            signature=payment_in.signature,
            amount=payment_in.amount,
        )
        await self.account_repo.update_balance(
            account_id=account.id,
            amount=payment_in.amount,
        )

        return PaymentOut.model_validate(payment)

    async def get_all_user_payments(self, user_id: int) -> PaymentsList:
        """
        Получить все платежи активного пользователя по user_id.

        :param user_id: Идентификатор пользователя.
        :return: Список платежей в виде Pydantic-схемы PaymentsList.
        :raises PaymentNotFound: если платежи не найдены.
        """
        payments: Sequence[Payment] = await self.payment_repo.get_all_payments(
            user_id=user_id,
        )
        if not payments:
            raise PaymentNotFound()
        payments_out = [
            PaymentOut.model_validate(
                payment,
            )
            for payment in payments
        ]
        return PaymentsList(payments=payments_out)

"""Репозиторий для работы транзакциями платежей в базе данных."""

from sqlalchemy import Sequence, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi_app.models import Account, Payment


class PaymentRepo:
    """Репозиторий для CRUD операций с транзакциями."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализация сессии базы данных."""
        self.session = session

    async def get_all_payments(self, user_id: int) -> Sequence[Payment]:
        """Получить все транзакции пользователя."""
        smtp = (
            select(Payment)
            .options(joinedload(Payment.account))
            .join(Payment.account)
            .where(Account.user_id == user_id)
            .order_by(desc(Payment.created_at))
        )
        result = await self.session.execute(smtp)
        payments_orm = result.scalars().all()
        return payments_orm

    async def create_payment(
        self,
        transaction_id: str,
        account_id: int,
        signature: str,
        amount: float,
    ) -> Payment:
        """Создать новую транзакцию."""
        payment = Payment(
            transaction_id=transaction_id,
            account_id=account_id,
            signature=signature,
            amount=amount,
        )
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

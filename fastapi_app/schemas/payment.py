"""Схемы для платёжных транзакций."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PaymentConfig(BaseModel):
    """Модель конфигурации платежной транзакции."""

    transaction_id: str
    account_id: int
    amount: float


class CreatePayment(PaymentConfig):
    """Модель создаёт транзакцию."""

    user_id: int
    signature: str


class PaymentOut(PaymentConfig):
    """Модель демонстрации платежа."""

    model_config = ConfigDict(from_attributes=True)
    created_at: datetime


class PaymentsList(BaseModel):
    """Модель списка платежных транзакций."""

    model_config = ConfigDict(from_attributes=True)
    payments: list[PaymentOut]

"""Схемы для платёжных транзакций."""

import hashlib
import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

from fastapi_app.configs import settings


class PaymentConfig(BaseModel):
    """Модель конфигурации платежной транзакции."""

    transaction_id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid.uuid4()),
            description="ID транзакции. Если не передан — генерируется автоматически.",
        ),
    ]
    account_id: Annotated[int, Field(description="ID счёта получателя")]
    amount: Annotated[float, Field(description="Сумма платежа")]
    signature: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "Подпись запроса. Если не указана — вычисляется автоматически по алгоритму: "
                "sha256(account_id + amount + transaction_id + user_id + secret_key)."
            ),
        ),
    ]

    @model_validator(mode="after")
    def generate_signature_if_missing(cls, model):
        """Генерация сигнатуры."""
        if model.signature is None:
            raw = (
                f"{model.account_id}"
                f"{model.amount:.2f}"
                f"{model.transaction_id}"
                f"{model.user_id}"
                f"{settings.secret.key}"
            )
            model.signature = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return model


class CreatePayment(PaymentConfig):
    """Модель создаёт транзакцию."""

    user_id: Annotated[int, Field(description="ID пользователя")]


class PaymentOut(PaymentConfig):
    """Модель демонстрации платежа для администрирования."""

    model_config = ConfigDict(from_attributes=True)
    created_at: datetime


class PaymentsList(BaseModel):
    """Модель списка платежных транзакций."""

    model_config = ConfigDict(from_attributes=True)
    payments: list[PaymentOut]

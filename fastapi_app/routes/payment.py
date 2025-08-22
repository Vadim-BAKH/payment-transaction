"""Модуль для маршрутов платёжных транзакций."""

from fastapi import APIRouter, Depends, status

from fastapi_app.dependencies.get_payment import get_payment_service
from fastapi_app.schemas.payment import CreatePayment, PaymentOut
from fastapi_app.services import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    "/webhook",
    response_model=PaymentOut,
    status_code=status.HTTP_201_CREATED,
)
async def webhook_payment(
    payment: CreatePayment,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentOut:
    """Эмуляция вебхука от платёжной системы."""
    return await service.create_payment_and_update_balance(payment)

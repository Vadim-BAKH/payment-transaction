"""Модуль для маршрутов платёжных транзакций."""

from fastapi import APIRouter, Depends, status

from fastapi_app.dependencies import (
    CurrActiveUser,
    get_payment_service,
)
from fastapi_app.schemas.payment import (
    CreatePayment,
    PaymentOut,
    PaymentsList,
)
from fastapi_app.services import PaymentService

router = APIRouter(prefix="/payments", tags=["Payment"])


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


@router.get(
    "/look",
    response_model=PaymentsList,
    status_code=status.HTTP_200_OK,
)
async def get_all_user_payment(
    user: CurrActiveUser,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentsList:
    """Получение всех транзакций текущего пользователя."""
    return await service.get_all_user_payments(user_id=user.id)

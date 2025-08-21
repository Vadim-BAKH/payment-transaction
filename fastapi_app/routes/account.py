"""Роутер для управления счетами пользователя."""

from fastapi import APIRouter, Depends, status

from fastapi_app.dependencies import (
    get_account_service,
)
from fastapi_app.schemas import (
    AccountCreate,
    AccountOut,
)
from fastapi_app.services import AccountService

router = APIRouter(prefix="/accounts", tags=["Account"])


@router.post(
    "/create",
    response_model=AccountOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    account: AccountCreate,
    # _: None = Depends(check_permission("super", "main")),
    service: AccountService = Depends(get_account_service),
):
    """Получение списка заявок."""
    return await service.create_user_account(user_in=account)


# @router.post(
#     "/",
#     response_model=OrderOut,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_order(
#     order: OrderCreate,
#     _: None = Depends(check_permission("orders", "create")),
#     service: OrderService = Depends(get_order_service),
# ):
#     """Создание заявки."""
#     return await service.create_order(order)
#
#
# @router.delete(
#     "/{order_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_order(
#     order_id: UUID,
#     _: None = Depends(check_permission("orders", "delete")),
#     service: OrderService = Depends(get_order_service),
# ):
#     """Удаление заявки по ID."""
#     await service.delete_order(order_id)

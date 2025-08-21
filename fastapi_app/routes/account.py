"""Роутер для управления счетами пользователя."""

from fastapi import APIRouter, Depends, status

from fastapi_app.dependencies import (
    CurrActiveUser,
    get_account_service,
)
from fastapi_app.schemas import (
    AccountCreate,
    AccountOut,
    AccountsList,
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
    """Создание счёта пользователя."""
    return await service.create_user_account(user_in=account)


@router.get(
    "/look",
    response_model=AccountsList,
    status_code=status.HTTP_200_OK,
)
async def get_user_accounts(
    user: CurrActiveUser,
    service: AccountService = Depends(get_account_service),
) -> AccountsList:
    """Получения списка активных счетов текущего пользователя."""
    return await service.get_all_user_accounts(user_id=user.id)


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

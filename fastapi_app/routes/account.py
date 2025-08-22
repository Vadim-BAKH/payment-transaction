"""Роутер для управления счетами пользователя."""

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

from fastapi_app.dependencies import (
    CurrActiveUser,
    check_permission,
    get_account_service,
    get_info_users_accounts_service,
)
from fastapi_app.schemas import (
    AccountCreate,
    AccountOut,
    AccountsList,
    ListAllUserInfoOut,
)
from fastapi_app.services import (
    AccountService,
    AllUserInfoService,
)

router = APIRouter(prefix="/accounts", tags=["Account"])


@router.post(
    "/create",
    response_model=AccountOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    account: AccountCreate,
    _: None = Depends(check_permission("super", "main")),
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


@router.get(
    "/users",
    response_model=ListAllUserInfoOut,
    status_code=status.HTTP_200_OK,
)
async def get_all_users_accounts(
    params: Params = Depends(),
    _: None = Depends(check_permission("super", "main")),
    service: AllUserInfoService = Depends(get_info_users_accounts_service),
) -> ListAllUserInfoOut:
    """Получения списка активных счетов текущего пользователя."""
    return await service.get_all_users_info(params=params)

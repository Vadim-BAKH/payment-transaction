"""Роутер для регистрации пользователей и аутентификации."""

from fastapi import APIRouter, Body, Depends, status

from fastapi_app.dependencies import (
    CurrActiveUser,
    check_permission,
    get_user_service,
)
from fastapi_app.schemas import (
    UserCreate,
    UserOut,
    UserUpdate,
)
from fastapi_app.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate,
    _: None = Depends(check_permission("super", "main")),
    service: UserService = Depends(get_user_service),
):
    """
    Регистрация нового пользователя.

    Доступно только администратору.
    """
    user = await service.register_user(user_in=user_in)
    return user


@router.get(
    "/users/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def get_auth_user_self_info(
    user: CurrActiveUser,
) -> UserOut:
    """
    Возвращает информацию о текущем авторизованном пользователе.

    Требуется валидный JWT-токен.
    """
    return UserOut.model_validate(user)


@router.patch(
    "/users/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
async def update_user_by_id(
    user_id: int,
    user_update: UserUpdate = Body(...),
    _: None = Depends(check_permission("super", "main")),
    user_service: UserService = Depends(get_user_service),
):
    """
    Обновление информации о пользователе.

    Поля, которые не переданы — не изменятся.
    Доступно только администратору.
    """
    updated_user = await user_service.update_user_by_id(
        user_id=user_id,
        user_update=user_update,
    )
    return UserOut.model_validate(updated_user)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_id(
    user_id: int,
    _: None = Depends(check_permission("super", "main")),
    user_service: UserService = Depends(get_user_service),
):
    """
    Удаление (деактивация) пользователя по ID.

    Доступно только администратору.
    """
    await user_service.delete_user_by_id(user_id=user_id)

"""Модуль сериализует полную информацию по пользователям."""

from fastapi_pagination import Page
from pydantic import BaseModel, ConfigDict

from fastapi_app.schemas.account import AccountOut
from fastapi_app.schemas.user import UserOut


class UserAllInfoConfig(BaseModel):
    """
    Модель информации о пользователях.

    Сериализует данные и состояние платежных счетов.
    """

    model_config = ConfigDict(from_attributes=True)
    user: UserOut
    account: AccountOut


class PaginateAllUsersInfo(Page[UserAllInfoConfig]):
    """
    Схема пагинированного списка пользователей и их счетов..

    Наследует стандартную схему пагинации fastapi_pagination Page.
    Предоставляет пагинированный вывод объектов UserAllInfoConfig.
    """

    model_config = ConfigDict(from_attributes=True)

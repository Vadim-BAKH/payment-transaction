"""Модуль общего представления пользователей."""

from fastapi_pagination import Page
from pydantic import BaseModel, ConfigDict

from fastapi_app.schemas.account import AccountsList
from fastapi_app.schemas.user import UserOut


class AllUserInfoOut(BaseModel):
    """Модель представляет информацию о пользователе и его счетах."""

    model_config = ConfigDict(from_attributes=True)
    user: UserOut
    accounts: AccountsList


class ListAllUserInfoOut(BaseModel):
    """Модель пагинированного списка пользователей со счетами."""

    model_config = ConfigDict(from_attributes=True)
    info: Page[AllUserInfoOut]

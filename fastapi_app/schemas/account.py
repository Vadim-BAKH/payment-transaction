"""Схемы для балансового счета."""

from pydantic import BaseModel, ConfigDict


class AccountConfig(BaseModel):
    """Модель балансового счёта."""

    account_number: int
    balance: float = 0


class AccountCreate(AccountConfig):
    """Модель создания счёта."""


class AccountOut(AccountConfig):
    """Модель демонстрации счёта."""

    model_config = ConfigDict(from_attributes=True)
    is_active: bool


class AccountsList(BaseModel):
    """Модель демонстрации списка счетов."""

    model_config = ConfigDict(from_attributes=True)
    accounts: list[AccountOut]

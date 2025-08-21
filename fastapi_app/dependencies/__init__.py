"""Инициализация зависимостей."""

__all__ = [
    "CurrentUser",
    "CurrRefreshUser",
]
from fastapi_app.dependencies.user_condition import (
    CurrentUser,
    CurrRefreshUser,
)

"""Инициализация зависимостей."""

__all__ = [
    "CurrentUser",
    "CurrRefreshUser",
    "DBSessionDep",
    "check_permission",
    "get_user_repo",
    "CurrActiveUser",
]
from fastapi_app.dependencies.check_permission import (
    check_permission,
)
from fastapi_app.dependencies.db_session import (
    DBSessionDep,
)
from fastapi_app.dependencies.get_user_repo import (
    get_user_repo,
)
from fastapi_app.dependencies.user_condition import (
    CurrActiveUser,
    CurrentUser,
    CurrRefreshUser,
)

"""Инициализация репозиториев."""

__all__ = [
    "UserRepo",
    "PermissionRepo",
    "RoleRepo",
    "ResourceRepo",
    "AccountRepo",
    "PaymentRepo",
    "AllUserInfoRepo",
]

from fastapi_app.repositories.account_repo import AccountRepo
from fastapi_app.repositories.all_info_repo import AllUserInfoRepo
from fastapi_app.repositories.payment_repo import PaymentRepo
from fastapi_app.repositories.permission_repo import PermissionRepo
from fastapi_app.repositories.resource_repo import ResourceRepo
from fastapi_app.repositories.role_repo import RoleRepo
from fastapi_app.repositories.user_repo import UserRepo

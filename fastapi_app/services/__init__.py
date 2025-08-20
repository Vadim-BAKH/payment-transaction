"""Инициализация сервисов."""

__all__ = [
    "AuthService",
    "UserService",
    "PermissionService",
    "AccountService",
    "PaymentService",
]
from fastapi_app.services.account_service import AccountService
from fastapi_app.services.auth_service import AuthService
from fastapi_app.services.payment_servise import PaymentService
from fastapi_app.services.permission import PermissionService
from fastapi_app.services.user_service import UserService

"""Инициализация маршрутов."""

__all__ = [
    "jwt_rout",
    "admin_dist_rout",
    "auth_rout",
    "account_rout",
]

from fastapi_app.routes.account import router as account_rout
from fastapi_app.routes.admin_distribution import router as admin_dist_rout
from fastapi_app.routes.auth import router as auth_rout
from fastapi_app.routes.jwt import router as jwt_rout

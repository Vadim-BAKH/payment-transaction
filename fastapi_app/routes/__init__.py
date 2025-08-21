"""Инициализация маршрутов."""

__all__ = [
    "jwt_rout",
]

from fastapi_app.routes.jwt import router as jwt_rout

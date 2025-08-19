"""Инициализация моделей."""

__all__ = [
    "Base",
    "User",
    "Role",
    "Permission",
    "RolePermission",
    "Resource",
    "UserRole",
    "IntIdPkMixin",
    "NameMixin",
    "DescriptionMixin",
]

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.description_mix import DescriptionMixin
from fastapi_app.models.mixins.name_mix import NameMixin
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin
from fastapi_app.models.permission import Permission
from fastapi_app.models.resource import Resource
from fastapi_app.models.role import Role
from fastapi_app.models.role_permission import RolePermission
from fastapi_app.models.user import User
from fastapi_app.models.user_role import UserRole

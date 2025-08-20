"""Инициализация моделей pydentic."""

__all__ = [
    "UserBase",
    "UserCreate",
    "UserOut",
    "UserUpdate",
    "LoginRequest",
    "LoginResponse",
    "TokenPayload",
    "TokenInfo",
    "PermissionOut",
    "PermissionCreate",
    "RoleCreate",
    "RoleOut",
    "ResourceOut",
    "ResourceCreate",
    "AccountCreate",
    "AccountsList",
    "CreatePayment",
    "PaymentsList",
    "UserAllInfoConfig",
    "PaginateAllUsersInfo",
    "AccountOut",
]

from fastapi_app.schemas.account import (
    AccountCreate,
    AccountOut,
    AccountsList,
)
from fastapi_app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    TokenInfo,
    TokenPayload,
)
from fastapi_app.schemas.payment import (
    CreatePayment,
    PaymentsList,
)
from fastapi_app.schemas.permission import (
    PermissionCreate,
    PermissionOut,
)
from fastapi_app.schemas.resource import (
    ResourceCreate,
    ResourceOut,
)
from fastapi_app.schemas.role import (
    RoleCreate,
    RoleOut,
)
from fastapi_app.schemas.user import (
    UserBase,
    UserCreate,
    UserOut,
    UserUpdate,
)
from fastapi_app.schemas.users_info import (
    PaginateAllUsersInfo,
    UserAllInfoConfig,
)

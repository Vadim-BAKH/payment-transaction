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
    "AccountOut",
    "PaymentOut",
    "ListAllUserInfoOut",
    "AllUserInfoOut",
]

from fastapi_app.schemas.account import (
    AccountCreate,
    AccountOut,
    AccountsList,
)
from fastapi_app.schemas.all_users_position import (
    AllUserInfoOut,
    ListAllUserInfoOut,
)
from fastapi_app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    TokenInfo,
    TokenPayload,
)
from fastapi_app.schemas.payment import (
    CreatePayment,
    PaymentOut,
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

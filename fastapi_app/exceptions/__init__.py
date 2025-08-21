"""Инициализация исключений c базовым классом HTTPException."""

__all__ = [
    "register_exception_handler",
    "PasswordsDoNotMatch",
    "EmailExists",
    "NotAccessTokenType",
    "NotRefreshTokenType",
    "NoUserByThisId",
    "UserUnauthorized",
    "InvalidToken",
    "UserInActive",
    "UserNotFound",
    "NotRightEnough",
    "ResourceNotFound",
    "BadAccountNumber",
    "AccountNotFound",
    "PaymentNotFound",
    "InvalidSignature",
    "TransactionAlreadyProcessed",
]

from fastapi_app.exceptions.detail_exc.bad_request import (
    BadAccountNumber,
    EmailExists,
    InvalidSignature,
    PasswordsDoNotMatch,
)
from fastapi_app.exceptions.detail_exc.conflict import (
    TransactionAlreadyProcessed,
)
from fastapi_app.exceptions.detail_exc.forbidden import (
    NotRightEnough,
    UserInActive,
)
from fastapi_app.exceptions.detail_exc.not_found import (
    AccountNotFound,
    NoUserByThisId,
    PaymentNotFound,
    ResourceNotFound,
    UserNotFound,
)
from fastapi_app.exceptions.detail_exc.unauthorized import (
    InvalidToken,
    NotAccessTokenType,
    NotRefreshTokenType,
    UserUnauthorized,
)
from fastapi_app.exceptions.general_exc import register_exception_handler

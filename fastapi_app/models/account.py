"""Модель платёжного счёта пользователя."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin
from fastapi_app.models.mixins.soft_delete import ActiveMixin

if TYPE_CHECKING:
    from fastapi_app.models.payment import Payment
    from fastapi_app.models.user import User


class Account(IntIdPkMixin, ActiveMixin, Base):
    """Модель счета и баланса для пользователя."""

    __tablename__ = "accounts"

    balance: Mapped[float] = mapped_column(
        Float,
        default=0,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="accounts",
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="account",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return (
            f"<Account(id={self.id!r}, "
            f"balance={self.balance!r}, "
            f"user_id={self.user_id!r})>"
        )

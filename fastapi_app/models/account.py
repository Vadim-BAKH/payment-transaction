"""Модель платёжного счёта пользователя."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.created_at_mix import CreatedAtMixin
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin
from fastapi_app.models.mixins.soft_delete import ActiveMixin

if TYPE_CHECKING:
    from fastapi_app.models.payment import Payment
    from fastapi_app.models.user import User


class Account(IntIdPkMixin, CreatedAtMixin, ActiveMixin, Base):
    """Модель счета и баланса для пользователя."""

    __tablename__ = "accounts"

    balance: Mapped[float] = mapped_column(
        Float,
        default=0,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
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

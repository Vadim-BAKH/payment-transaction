"""Модель платежа."""

from typing import TYPE_CHECKING

from sqlalchemy import (
    Float,
    ForeignKey,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.created_at_mix import CreatedAtMixin

if TYPE_CHECKING:
    from fastapi_app.models.account import Account


class Payment(CreatedAtMixin, Base):
    """Модель транзакции платежа."""

    __tablename__ = "payments"

    transaction_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False,
    )
    signature: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(
        Float,
        default=0,
    )
    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="payments",
    )
    __table_args__ = (PrimaryKeyConstraint("account_id", "transaction_id"),)

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return (
            f"<Payment(account_id={self.account_id!r}, "
            f"transaction_id={self.transaction_id!r}, "
            f"amount={self.amount!r})>"
        )

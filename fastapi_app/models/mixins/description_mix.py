"""Модель миксин description."""

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class DescriptionMixin:
    """Модель определяет общее поле description."""

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

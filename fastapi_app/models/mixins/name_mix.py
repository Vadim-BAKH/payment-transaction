"""Модель миксин name."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class NameMixin:
    """Модель определяет общее поле name."""

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

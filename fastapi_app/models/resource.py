"""Модель ресурса."""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.description_mix import DescriptionMixin
from fastapi_app.models.mixins.name_mix import NameMixin
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin

if TYPE_CHECKING:
    from fastapi_app.models.permission import Permission


class Resource(IntIdPkMixin, NameMixin, DescriptionMixin, Base):
    """Модель ресурса, к которому привязываются разрешения."""

    __tablename__ = "resources"

    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        back_populates="resource",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<Resource(id={self.id}, name={self.name!r})>"

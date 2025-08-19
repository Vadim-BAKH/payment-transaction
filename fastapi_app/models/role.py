"""Модель роли."""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.description_mix import DescriptionMixin
from fastapi_app.models.mixins.name_mix import NameMixin
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin

if TYPE_CHECKING:
    from fastapi_app.models.role_permission import RolePermission
    from fastapi_app.models.user_role import UserRole


class Role(IntIdPkMixin, NameMixin, DescriptionMixin, Base):
    """Модель роли, объединяющая пользователей и разрешения."""

    __tablename__ = "roles"

    users: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )
    permissions: Mapped[list["RolePermission"]] = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return f"<Role(id={self.id}, name={self.name!r})>"

"""Промежуточная модель для полей и разрешений."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin

if TYPE_CHECKING:
    from fastapi_app.models.permission import Permission
    from fastapi_app.models.role import Role


class RolePermission(IntIdPkMixin, Base):
    """Связывающая модель между ролями и разрешениями."""

    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
    )
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"),
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="permissions",
    )
    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="roles",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return (
            f"<RolePermission(id={self.id}, role_id={self.role_id}, "
            f"permission_id={self.permission_id})>"
        )

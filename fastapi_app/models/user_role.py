"""Промежуточная модель для пользователей и ролей."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_app.models.base import Base
from fastapi_app.models.mixins.pk_mix import IntIdPkMixin

if TYPE_CHECKING:
    from fastapi_app.models.role import Role
    from fastapi_app.models.user import User


class UserRole(IntIdPkMixin, Base):
    """Связывающая модель между пользователями и ролями."""

    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="roles",
    )
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users",
    )

    def __repr__(self) -> str:
        """Строковое представление модели."""
        return (
            f"<UserRole(id={self.id},"
            f" user_id={self.user_id},"
            f" role_id={self.role_id},)>"
        )

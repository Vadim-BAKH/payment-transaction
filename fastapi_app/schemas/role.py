"""Схемы для ролей."""

from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    """Модель создания роли."""

    name: str
    description: str | None = None


class RoleOut(RoleCreate):
    """Модель получения роли."""

    id: int

    model_config = ConfigDict(from_attributes=True)

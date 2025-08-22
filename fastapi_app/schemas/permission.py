"""Схемы для прав доступа к ресурсам."""

from pydantic import BaseModel, ConfigDict


class PermissionCreate(BaseModel):
    """Модель создания права."""

    resource: str  # по имени ресурса
    action: str


class PermissionOut(PermissionCreate):
    """Модель представления права."""

    id: int

    model_config = ConfigDict(from_attributes=True)

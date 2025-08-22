"""Схемы для ресурса."""

from pydantic import BaseModel, ConfigDict


class ResourceCreate(BaseModel):
    """Модель создания ресурса."""

    name: str
    description: str | None = None


class ResourceOut(ResourceCreate):
    """Модель просмотра ресурса."""

    id: int

    model_config = ConfigDict(from_attributes=True)

"""Модуль сервиса работы с пользователями."""

from fastapi_app.authentication import hash_password
from fastapi_app.exceptions import EmailExists
from fastapi_app.models import User
from fastapi_app.repositories import UserRepo
from fastapi_app.schemas import UserCreate, UserUpdate


class UserService:
    """Сервис для управления логикой пользователей."""

    def __init__(self, user_repo: UserRepo):
        """Инициализация с репозиторием пользователей."""
        self.user_repo = user_repo

    async def register_user(self, user_in: UserCreate) -> User:
        """Регистрация нового пользователя с хешированием пароля."""
        if await self.user_repo.exists_by_email(user_in.email):
            raise EmailExists()
        data = user_in.model_dump(exclude={"password_confirm"})
        hashed_password = hash_password(user_in.password.get_secret_value())
        data["password"] = hashed_password
        user = await self.user_repo.create(**data)
        return user

    async def update_user_by_id(
        self,
        user_id: int,
        user_update: UserUpdate,
    ) -> User:
        """Обновить данные пользователя по ID, включая хеширование пароля."""
        update_data = user_update.model_copy(deep=True)
        if update_data.password:
            update_data.password = hash_password(
                update_data.password.get_secret_value(),
            )
        return await self.user_repo.update_by_id(
            user_id=user_id,
            **update_data.model_dump(exclude_unset=True),
        )

    async def delete_user_by_id(self, user_id: int) -> None:
        """Деактивировать пользователя по ID (мягкое удаление)."""
        await self.user_repo.delete_by_id(user_id)

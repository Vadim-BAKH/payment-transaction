"""Создание суперпользователя, пользователя, счёт при запуске приложения."""

import asyncio
import logging

from sqlalchemy import and_, exists, select

from fastapi_app.configs import async_session, settings
from fastapi_app.models import RolePermission, UserRole
from fastapi_app.repositories import (
    AccountRepo,
    PermissionRepo,
    ResourceRepo,
    RoleRepo,
    UserRepo,
)
from fastapi_app.schemas import (
    AccountCreate,
    PermissionCreate,
    ResourceCreate,
    RoleCreate,
    UserCreate,
)
from fastapi_app.services import AccountService, UserService

log = logging.getLogger(__name__)


async def create_superuser():
    """Создаёт суперпользователя с ролью и правами."""
    async with async_session() as session:
        # Репозитории
        user_repo = UserRepo(session)
        resource_repo = ResourceRepo(session)
        permission_repo = PermissionRepo(session)
        role_repo = RoleRepo(session)

        user_service = UserService(user_repo)

        # Создание суперпользователя
        user_data = UserCreate(
            email=settings.superuser.email,
            password=settings.superuser.password,
            password_confirm=settings.superuser.password,
            first_name=settings.superuser.first_name,
            last_name=settings.superuser.last_name,
        )

        user = await user_service.user_repo.get_by_email(user_data.email)
        if user:
            log.info("Суперпользователь уже существует: %s", user.email)
        else:
            user = await user_service.register_user(user_data)
            log.info("Суперпользователь создан: %s", user.email)

        # Создание ресурса
        resource = await resource_repo.get_by_name("super")
        if not resource:
            resource = await resource_repo.create(
                ResourceCreate(name="super"),
            )

        # Создание permission
        permission = await permission_repo.get_by_action_and_resource(
            action="main",
            resource_name=resource.name,
        )
        if not permission:
            permission = await permission_repo.create(
                PermissionCreate(resource=resource.name, action="main"),
            )

        # Создание роли
        role = await role_repo.get_by_name("superuser")
        if not role:
            role = await role_repo.create(RoleCreate(name="superuser"))

            # Привязать permission к роли
            session.add(
                RolePermission(role_id=role.id, permission_id=permission.id),
            )
            await session.commit()

        # Назначение роли пользователю
        existing = await session.scalar(
            select(
                exists().where(
                    and_(
                        UserRole.user_id == user.id,
                        UserRole.role_id == role.id,
                    ),
                ),
            ),
        )
        if not existing:
            session.add(UserRole(user_id=user.id, role_id=role.id))
            await session.commit()
            log.info("Роль superuser назначена пользователю %s", user.email)
        else:
            log.info(
                "Роль superuser уже назначена пользователю %s",
                user.email,
            )


async def create_user_and_account():
    """Создаёт пользователя и балансовый счёт."""
    async with async_session() as session:
        user_repo = UserRepo(session=session)
        user_service = UserService(user_repo=user_repo)
        account_repo = AccountRepo(session=session)
        account_service = AccountService(account_repo=account_repo)

        user_data = UserCreate(
            email=settings.test_user.email,
            password=settings.test_user.password,
            password_confirm=settings.test_user.password,
            first_name=settings.test_user.first_name,
            last_name=settings.test_user.last_name,
        )

        user = await user_service.user_repo.get_by_email(user_data.email)
        if user:
            log.info("Пользователь уже существует: %s", user.email)
        else:
            user = await user_service.register_user(user_data)
            log.info("Пользователь создан: %s", user.email)
            account_data = AccountCreate(user_id=user.id)
            account = await account_service.create_user_account(
                user_in=account_data,
            )
            log.info(
                "Счёт создан для пользователя %s, счет id: %s",
                user.email,
                account.id,
            )


async def main():
    """Вызов асинхронных событий."""
    await create_superuser()
    await create_user_and_account()


if __name__ == "__main__":
    asyncio.run(main())

"""Модуль проверяет право пользователя на действие."""

from fastapi_app.dependencies.db_session import DBSessionDep
from fastapi_app.dependencies.user_condition import CurrActiveUser
from fastapi_app.exceptions import NotRightEnough
from fastapi_app.repositories import PermissionRepo
from fastapi_app.services import PermissionService


def check_permission(resource: str, action: str):
    """
    Создаёт зависимость для проверки разрешения пользователя на действие с ресурсом.

    :param resource: Имя ресурса, для которого проверяется разрешение.
    :param action: Действие, на которое проверяется разрешение.
    :return: Асинхронная функция зависимость для проверки прав.
    """

    async def _check_permission(
        user: CurrActiveUser,
        session: DBSessionDep,
    ) -> None:
        """
        Проверяет, имеет ли пользователь права на требуемое действие.

        :param user: Текущий активный пользователь.
        :param session: Асинхронная сессия базы данных.
        :raises NotRightEnough: Если прав недостаточно, выбрасывает исключение.
        :return: None при успешной проверке.
        """
        repo = PermissionRepo(session=session)
        service = PermissionService(permission_repo=repo)

        has_perm = await service.has_permission(user, resource, action)
        if not has_perm:
            raise NotRightEnough
        return None  # Внутренняя должна возвращать None

    return _check_permission  # Внешняя возвращает функцию

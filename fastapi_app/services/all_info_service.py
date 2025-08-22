"""Модуль сервиса получения полной информации."""

from fastapi_pagination import Page, Params

from fastapi_app.repositories import AllUserInfoRepo
from fastapi_app.schemas import AllUserInfoOut, ListAllUserInfoOut


class AllUserInfoService:
    """Сервис для агрегации пользователь + счета."""

    def __init__(self, info_repo: AllUserInfoRepo):
        self.info_repo = info_repo

    async def get_all_users_info(self, params: Params) -> ListAllUserInfoOut:
        """
        Вернуть пагинированный список пользователей со счетами.

        :param params: Параметры пагинации (page, size)
        :return: Страница AllUserInfoOut
        """
        src_page = await self.info_repo.get_users_balance_position(params)

        items = [
            AllUserInfoOut.model_validate(
                {
                    "user": user,
                    "accounts": {"accounts": list(user.accounts)},
                },
            )
            for user in src_page.items
        ]

        new_page = Page.create(
            items=items,
            total=src_page.total,
            params=params,
        )

        return ListAllUserInfoOut.model_validate(new_page)

"""Модуль для локального запуска приложения при разработке."""

import asyncio
import logging
import sys

import uvicorn

import fastapi_app.init

log = logging.getLogger(__name__)


async def run_init_module():
    """Вызов корутины инициализации приложения."""
    await fastapi_app.init.main()


async def run_alembic_upgrade():
    """Асинхронный запуск миграций Alembic."""
    process = await asyncio.create_subprocess_exec(
        "alembic",
        "upgrade",
        "head",
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    return_code = await process.wait()
    if return_code != 0:
        raise RuntimeError(
            f"Alembic migration failed with code {return_code}",
        )
    log.info("Alembic migration applied.")


async def main():
    """Запуск миграций, инициализации и сервера Uvicorn."""
    await run_alembic_upgrade()
    await run_init_module()

    uvicorn.run(
        "fastapi_app.app:app_",
        host="0.0.0.0",  # nosec B104
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    asyncio.run(main())

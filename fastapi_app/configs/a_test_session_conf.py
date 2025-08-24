"""Настройки тестового и движка и сессий."""

import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_app.configs.main_conf import settings

log = logging.getLogger(__name__)

log.debug("Connecting to test database %s:", settings.url_test.uri)
async_test_engine = create_async_engine(settings.url_test.uri)
async_test_session = async_sessionmaker(
    bind=async_test_engine,
    expire_on_commit=False,
)

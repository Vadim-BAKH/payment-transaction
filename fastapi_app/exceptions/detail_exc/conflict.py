"""Модели обработки исключений 'HTTP_409_CONFLICT'."""

from fastapi import HTTPException, status


class TransactionAlreadyProcessed(HTTPException):
    """Модель исключения 'TransactionAlreadyProcessed'."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transaction already processed",
        )

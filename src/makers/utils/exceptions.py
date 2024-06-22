from typing import Any

from fastapi import Request
from starlette import status
from sqlalchemy.exc import NoResultFound  # noqa
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


class BaseAPIException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Произошла ошибка сервера."

    def __init__(self, status_code: int = None, detail: Any = None):
        _status_code = status_code or self.status_code
        _detail = detail or self.default_detail
        super(BaseAPIException, self).__init__(
            status_code=_status_code,
            detail=_detail
        )


class PermissionDenied(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "У вас нету прав для выполнение этого действия."


class NotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Не найдена"


async def not_found_exception_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Не найдена"}
    )

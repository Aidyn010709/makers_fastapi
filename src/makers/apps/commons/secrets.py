import jwt

from datetime import timedelta, datetime
from typing import Union, Any, Dict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from makers.config.settings import settings
from makers.apps.auth.blocklist.services import get_jti_by_token


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Функция генерирует JWT токен"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Функция генерирует JWT токен"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def verify_access_token(
    db: AsyncSession, token: str
) -> Union[bool, Dict[str, Any]]:
    """Функция проверят на валидность токена. Если токен не валидный, то возвращает `False`"""
    jti_in_blocklist = await get_jti_by_token(db, jti=token)
    if jti_in_blocklist:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

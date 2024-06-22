import jwt
from starlette import status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Header

from makers.apps.auth import schemas
from makers.apps.commons import secrets
from makers.apps.auth.models import User
from makers.apps.db.deps import get_db_session
from makers.apps.commons.constants import CONSTANTS
from makers.apps.auth.selectors import get_org_user_detail


async def get_user_session(
    db: AsyncSession = Depends(get_db_session),
    *,
    token: str = Header(...)
) -> User:
    try:
        payload = await secrets.verify_access_token(db, token)
        schema = schemas.TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CONSTANTS.INVALID_TOKEN,
        )
    org_user = await get_org_user_detail(db, pk=schema.sub)
    if not org_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CONSTANTS.USER_NOT_FOUND,
        )
    return org_user

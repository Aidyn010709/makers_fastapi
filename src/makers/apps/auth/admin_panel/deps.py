import jwt

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Header, status

from makers.apps.commons import secrets
from makers.apps.auth.models import User
from makers.apps.auth.schemas import TokenPayload
from makers.apps.db.deps import get_db_session
from makers.apps.commons.constants import CONSTANTS
from makers.apps.auth.selectors import get_org_user_detail


async def get_admin_session(
    db: AsyncSession = Depends(get_db_session),
    *,
    token: str = Header(...)
) -> User:
    try:
        payload = await secrets.verify_access_token(db, token)
        schema = TokenPayload(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CONSTANTS.INVALID_TOKEN,
        )
    admin = await get_org_user_detail(db, pk=schema.sub, is_admin=True)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CONSTANTS.ONLY_ADMIN,
        )
    return admin

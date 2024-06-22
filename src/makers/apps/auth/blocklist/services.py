from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from makers.apps.auth.blocklist.models import TokenBlocklist
from makers.apps.commons.constants import get_current_time


async def add_to_blocklist(db: AsyncSession, *, jti: str, user_id: int):
    blocklist = TokenBlocklist(jti=jti, created_at=get_current_time(), user_id=user_id)
    db.add(blocklist)
    await db.commit()


async def get_jti_by_token(
        db: AsyncSession,
        *,
        jti: str,
):
    query = select(TokenBlocklist).filter(TokenBlocklist.jti == jti)
    blocklist = await db.execute(query)
    return blocklist.scalar_one_or_none()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from makers.apps.auth.models import User


async def get_liked_contacts(db, user_id):
    query = select(User).where(User.liked_by.contains([user_id]))
    result = await db.execute(query)
    liked_contacts = result.scalars().all()
    return liked_contacts
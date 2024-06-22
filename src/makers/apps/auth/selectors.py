from sqlalchemy.orm import selectinload
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from makers.apps.auth.models import User


async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    query = select(User).filter(User.email == email).order_by(desc(User.id))
    user = await db.execute(query)
    return user.scalar_one_or_none()


async def get_user_by_id(
    db: AsyncSession,
    *,
    user_id: int
):
    stmt = select(User).filter(User.id == user_id)
    query = await db.execute(stmt)
    user = query.scalar_one_or_none()
    return user


async def get_users_by_ids(
    db: AsyncSession,
    *,
    users_ids: list[int]
):
    query = select(User).filter(User.id.in_(users_ids))
    users = await db.execute(query)
    return users.scalars().all()


async def get_org_user_detail(
    db: AsyncSession,
    *,
    pk: int,
    is_admin: bool = False
) -> User | None:
    query = select(User).filter(
        and_(
            User.id == pk,
            User.is_active.is_(True),
            User.is_admin.is_(is_admin),
        ))
    org_user = await db.execute(query)
    user = org_user.scalar_one_or_none()

    return user

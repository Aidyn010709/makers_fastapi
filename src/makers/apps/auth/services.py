import string
import secrets

from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from makers.apps.commons.constants import get_current_time
from makers.apps.broker.decorator import PublisherWrapper
from makers.apps.events.schemas import EventTypes
from makers.apps.auth.models import User

@PublisherWrapper(event_type=EventTypes.SIGN_UP.value)
async def create_user(
    db: AsyncSession,
    *,
    name: str,
    last_name: str,
    email: str,
    password: str,
) -> User:
    activation_code = await generate_activation_code(length=16)
    user = User(
        name=name,
        last_name=last_name,
        email=email,
        password=password,
        activation_code=activation_code,
    )
    user.registered_at = get_current_time()
    db.add(user)
    await db.flush()
    await db.commit()
    return user


async def generate_activation_code(length=6):
    """
    Generate a random activation code consisting of uppercase letters and digits.
    """
    characters = string.ascii_lowercase + string.digits
    activation_code = "".join(secrets.choice(characters) for _ in range(length))
    return activation_code


async def check_user_is_active(user: User) -> bool:
    return user.is_active


async def check_user_is_admin(user: User) -> bool:
    return user.is_admin


async def get_user_by_activation_code(db: AsyncSession, *, activation_code: str):
    stmt = select(User).filter(User.activation_code == activation_code)
    query = await db.execute(stmt)
    return query.scalar_one_or_none()


async def activate_user(db: AsyncSession, *, user: User):
    user.is_active = True
    user.activation_code = ""
    await db.commit()
    await db.refresh(user)
    return user


async def update_activation_code(db: AsyncSession, *, user: User) -> str:
    updated_activation_code = await generate_activation_code(length=10)
    user.activation_code = updated_activation_code
    user.is_active = False

    await db.commit()
    return updated_activation_code


async def update_password(db: AsyncSession, *, user: User, new_password: str):
    user.password = new_password
    user.is_active = True
    user.activation_code = ""
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_by_id(db: AsyncSession, *, user_id: int):
    query = delete(User).filter(User.id == user_id)
    await db.execute(query)
    await db.commit()


async def get_admin_privileges(
    db: AsyncSession,
    *,
    user: User,
):
    # Only for test period
    user.is_admin = True
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_privileges(
    db: AsyncSession,
    *,
    user: User,
):
    # Only for test period
    user.is_admin = False
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_by_email(db: AsyncSession, *, email: str):
    # Only for test period
    query = delete(User).filter(User.email == email)
    await db.execute(query)
    await db.commit()


async def update_user_is_active(db: AsyncSession, *, email: str):
    # Only for test period
    query = update(User).where(User.email == email).values(is_active=True)
    await db.execute(query)
    await db.commit()

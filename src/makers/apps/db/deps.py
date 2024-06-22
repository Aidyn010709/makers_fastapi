from typing import AsyncGenerator

from makers.apps.db.session import Session


async def get_db_session() -> AsyncGenerator:
    async with Session() as session:
        yield session

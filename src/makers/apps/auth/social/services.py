from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from makers.apps.auth.models import User
from fastapi import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from makers.apps.auth.models import User
from makers.apps.auth.social.services import like_user
from makers.apps.db.deps import get_db_session
from makers.apps.auth.deps import get_user_session
from makers.apps.auth.social.schemas import LikeRequest
from sqlalchemy import select
from sqlalchemy.sql.expression import any_
from makers.apps.auth.social.selectors import get_liked_contacts


router = APIRouter()

@router.post("/like")
async def like_user_endpoint(
    like_request: LikeRequest,
    current_user: User = Depends(get_user_session),
    db: AsyncSession = Depends(get_db_session)
):
    # Проверяем, что пользователь аутентифицирован
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Устанавливаем лайк пользователю с указанным идентификатором
    await like_user(db, current_user.id, like_request.user_id)

    # Фиксируем изменения в базе данных
    await db.commit()
    
    return {"message": "Like added successfully"}


@router.get("/contacts")
async def get_contacts_with_likes(
    current_user: User = Depends(get_user_session),
    db: AsyncSession = Depends(get_db_session)
):
    # Проверяем, что пользователь аутентифицирован
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Получаем список пользователей, которым пользователь поставил лайк
    liked_contacts = await get_liked_contacts(db, current_user.id)
    
    print("Liked contacts:", liked_contacts)  # Вывод для отладки
    
    return liked_contacts
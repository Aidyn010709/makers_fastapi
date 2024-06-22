from starlette import status
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from makers.apps.db.deps import get_db_session
from makers.apps.mentor.services import create_mentor, check_mentor_is_active
from makers.apps.mentor.selectors import get_mentor_by_email, \
    get_mentor_detail
from makers.apps.auth.blocklist.services import add_to_blocklist
from makers.apps.mentor.schemas import (RegisteredMentorSchema,
                                        MentorResponseSchema,
                                        )
from makers.apps.auth import schemas
from makers.apps.commons.secrets import (create_access_token,
                                           verify_access_token,
                                           create_refresh_token)
from makers.apps.mentor.models import Mentor
from makers.apps.mentor.deps import get_mentor_session

router = APIRouter()


@router.post("/sign-up", response_model=MentorResponseSchema)
async def sign_up(
    db: AsyncSession = Depends(get_db_session),
    *,
    data: RegisteredMentorSchema = Depends(RegisteredMentorSchema.as_form),
):
    mentor = await get_mentor_by_email(db, email=data.email)
    if mentor:
        raise HTTPException(status_code=400,
                            detail="Mentor with this email already exists")
    
    mentor = await create_mentor(db, mentor_data=data)
    return await get_mentor_detail(db, mentor_id=mentor.id)


@router.post("/login", response_model=schemas.ActivationCodeResponse)
async def login(
    db: AsyncSession = Depends(get_db_session),
    *,
    mentor_in: schemas.LoginUserSchema,
):
    mentor = await get_mentor_by_email(db, email=mentor_in.email)
    
    if not mentor:
        raise HTTPException(
            status_code=404,
            detail="Incorrect Email or Password"
        )
    
    if not mentor.verify_password(mentor_in.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect Email or Password"
        )
    is_active = await check_mentor_is_active(mentor)
    if not is_active:
        raise HTTPException(
            status_code=400,
            detail="Not active account"
        )
    
    return {
        "data": {
            "email": mentor.email,
            "access_token": create_access_token(subject=str(mentor.id)),
            "refresh_token": create_refresh_token(subject=str(mentor.id))
        }
    }
    

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    db: AsyncSession = Depends(get_db_session),
    *,
    token: str = Header(...),
    current_mentor: Mentor = Depends(get_mentor_session)
):
    verified = await verify_access_token(db, token)
    if verified:
        await add_to_blocklist(db, jti=token, user_id=current_mentor.id)
    
    return {
        "data": {}
        }

    
@router.get("/refresh",
            status_code=status.HTTP_200_OK,
            response_model=schemas.AccessTokenResponse)
async def refresh_token(current_mentor: Mentor = Depends(get_mentor_session)):
    access_token = create_access_token(subject=str(current_mentor.id))
    
    return {"access_token": access_token}

@router.get("/mentor/{mentor_id}", response_model=MentorResponseSchema)
async def get_mentor_details(
    mentor_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    mentor = await get_mentor_detail(db, mentor_id=mentor_id)
    if mentor is None:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor
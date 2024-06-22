from loguru import logger
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Path, Header

from makers.apps.commons import tasks
from makers.apps.auth.models import User
from makers.apps.auth import deps as auth_deps
from makers.apps.db.deps import get_db_session
from makers.apps.auth import schemas, selectors, services
from makers.apps.auth.admin_panel import deps as admin_deps
from makers.apps.auth.blocklist.services import add_to_blocklist
from makers.apps.services.emailjet_send.service import (
    send_activation_code,
    send_reset_password,
)
from makers.apps.commons.secrets import (
    create_access_token,
    verify_access_token,
    create_refresh_token,
)

auth_router = APIRouter()


@auth_router.post("/sign-up", response_model=schemas.UserInDB)
async def sign_up(
    db: AsyncSession = Depends(get_db_session),
    *,
    data: schemas.CreateUserSchema,
    background_task: BackgroundTasks,
) -> schemas.UserInDB:
    user = await selectors.get_user_by_email(db, email=data.email)

    if user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = await services.create_user(
        db,
        name=data.name,
        last_name=data.last_name,
        email=data.email,
        password=data.password,
    )
    background_task.add_task(
        send_activation_code,
        activation_code=user.activation_code,
        email=data.email,
        name=data.name,
    )
    background_task.add_task(tasks.free_trial_end_task, db, user=user)
    return user


@auth_router.get(
    "/activation-code/{activate_code}", response_model=schemas.ActivationCodeResponse
)
async def activation_code(
    db: AsyncSession = Depends(get_db_session),
    *,
    activate_code: str = Path(..., title="Код активации"),
):
    user: User | None = await services.get_user_by_activation_code(
        db, activation_code=activate_code
    )
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    await services.activate_user(db, user=user)

    return {
        "data": {
            "email": user.email,
            "access_token": create_access_token(subject=str(user.id)),
            "refresh_token": create_refresh_token(subject=str(user.id)),
        }
    }


@auth_router.post("/login", response_model=schemas.ActivationCodeResponse)
async def login(
    db: AsyncSession = Depends(get_db_session),
    *,
    user_in: schemas.LoginUserSchema,
):
    user = await selectors.get_user_by_email(db, email=user_in.email)

    if not user:
        raise HTTPException(status_code=404, detail="Incorrect Email or Password")

    if not user.verify_password(user_in.password):
        raise HTTPException(status_code=400, detail="Incorrect Email or Password")

    is_active = await services.check_user_is_active(user)
    if not is_active:
        raise HTTPException(status_code=400, detail="Please verify your email address")

    return {
        "data": {
            "email": user.email,
            "access_token": create_access_token(subject=str(user.id)),
            "refresh_token": create_refresh_token(subject=str(user.id)),
        }
    }


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    db: AsyncSession = Depends(get_db_session),
    *,
    token: str = Header(...),
    current_user: User = Depends(auth_deps.get_user_session),
):
    verified = await verify_access_token(db, token)
    if verified:
        await add_to_blocklist(db, jti=token, user_id=current_user.id)
    return {"data": {}}


@auth_router.get(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccessTokenResponse,
)
async def refresh_token(current_user: User = Depends(auth_deps.get_user_session)):
    access_token = create_access_token(subject=str(current_user.id))

    return {"access_token": access_token}


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    db: AsyncSession = Depends(get_db_session),
    *,
    data: schemas.ResetPasswordSchema,
    background_task: BackgroundTasks,
):
    user = await selectors.get_user_by_email(db, email=data.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    activation_code = await services.update_activation_code(db, user=user)

    background_task.add_task(
        send_reset_password,
        generate_activation_code=activation_code,
        email=user.email,
        name=user.name,
    )

    return {"data": {}}


@auth_router.post(
    "/complete-forgot-password/{activate_code}", status_code=status.HTTP_201_CREATED
)
async def reset_with_update_password(
    db: AsyncSession = Depends(get_db_session),
    *,
    reset: schemas.ResetUpdatePasswordSchema,
    activate_code: str = Path(..., title="Код активации"),
):
    user: User | None = await services.get_user_by_activation_code(
        db, activation_code=activate_code
    )
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    if reset.new_password != reset.new_password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password do not match"
        )
    await services.update_password(
        db,
        user=user,
        new_password=reset.new_password,
    )
    return {"data": {}}

@auth_router.post("/get-admin-privileges", status_code=status.HTTP_200_OK)
async def get_admin_privileges(
    db: AsyncSession = Depends(get_db_session),
    *,
    current_user: User = Depends(auth_deps.get_user_session),
):
    # Only for test period
    await services.get_admin_privileges(db, user=current_user)
    return {"data": {}}


@auth_router.post("/get-user-privileges", status_code=status.HTTP_200_OK)
async def get_user_privileges(
    db: AsyncSession = Depends(get_db_session),
    *,
    current_user: User = Depends(admin_deps.get_admin_session),
):
    # Only for test period
    await services.get_user_privileges(db, user=current_user)
    return {"data": {}}


@auth_router.post("/delete-user", status_code=status.HTTP_200_OK)
async def delete_user(
    db: AsyncSession = Depends(get_db_session),
    *,
    email: schemas.ResetPasswordSchema,
):
    # Only for test period
    await services.delete_user_by_email(db, email=email.email)
    return {"data": {}}


@auth_router.post("/activate-user", status_code=status.HTTP_200_OK)
async def activate_user(
    db: AsyncSession = Depends(get_db_session),
    *,
    email: schemas.ResetPasswordSchema,
):
    # Only for test period
    await services.update_user_is_active(db, email=email.email)
    return {"data": {}}

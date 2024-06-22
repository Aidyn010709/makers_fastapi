from typing import Optional, Union, List

from pydantic import BaseModel, Field, validator

from makers.apps.commons import constants
from makers.apps.commons.schemas import EmailBase


class RegisteredUserSchema(EmailBase):
    id: int
    name: Optional[str] = Field(title="Имя пользователя")
    last_name: Optional[str] = Field(title="Фамилия пользователя")
    phone_number: Optional[str] = Field(title="Номер телефона")


class BaseUserSchema(RegisteredUserSchema):
    role: str = Field(default=constants.RolesEnum.user.value, title="Роль")
    avatar: Optional[str] = Field(title="Аватар пользователя")


class UserResponse(BaseUserSchema):
    email: Optional[str] = Field(title="Почта пользователя")

    class Config:
        orm_mode = True


class CreateUserSchema(EmailBase):
    name: str = Field(title="Имя пользователя")
    last_name: str = Field(title="Фамилия пользователя")
    password: str = Field(title="Пароль пользователя", max_length=128, min_length=8)


class ActivationResponseData(EmailBase):
    access_token: str = Field(title="Token")
    refresh_token: str = Field(title="Token")


class ActivationCodeResponse(BaseModel):
    data: ActivationResponseData


class LoginUserSchema(EmailBase):
    password: str = Field(title="Пароль пользователя", max_length=128, min_length=8)


class UserInDB(RegisteredUserSchema):
    id: int

    class Config:
        orm_mode = True


class ResetPasswordSchema(EmailBase):
    pass


class ResetUpdatePasswordSchema(BaseModel):
    new_password: str = Field(
        title="Новый пароль пользователя", max_length=128, min_length=8
    )
    new_password_confirm: str = Field(
        title="Подтверждение нового пароля", max_length=128, min_length=8
    )


class TokenPayload(BaseModel):
    sub: Optional[Union[int, str]] = None

    @validator("sub")
    def validate_token(cls, v: Union[int, str]):
        if isinstance(v, int):
            return v
        if v.isdigit():
            return int(v)
        return v


class IDSubTokenPayload(TokenPayload):

    @validator("sub")
    def validate_token(cls, v: Union[int, str]):
        if isinstance(v, int):
            return v
        if v.isdigit():
            return int(v)
        else:
            raise ValueError("Не валидный токен доступа")


class AccessTokenResponse(BaseModel):
    access_token: str = Field(
        ...,
        regex=r"^[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_.+/=]*$",
    )

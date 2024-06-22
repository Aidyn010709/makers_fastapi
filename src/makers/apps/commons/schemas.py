from pydantic import BaseModel, EmailStr, Field


class EmailBase(BaseModel):
    email: EmailStr = Field(title="Email пользователя")

    class Config:
        orm_mode = True


class IDBase(BaseModel):
    id: int = Field(title="ID")

    class Config:
        orm_mode = True

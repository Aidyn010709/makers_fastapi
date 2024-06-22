from typing import List, Optional
from pydantic import BaseModel, Field
from makers.apps.commons.decorators import as_form
from makers.apps.commons.schemas import EmailBase
from makers.apps.mentor.constants import Education
from datetime import datetime

class DirectionBaseResponse(BaseModel):
    languages: Optional[List[str]] = Field(title="Язык программмирования")

    class Config:
        orm_mode = True


class ChooseSpecialitySchema(DirectionBaseResponse):
    speciality: str = Field(title="Направление")

    class Config:
        orm_mode = True

@as_form
class RegisteredMentorSchema(EmailBase):
    name: str = Field(title="Имя ментора")
    last_name: str = Field(title="Фамилия ментора")
    phone_number: Optional[str] = Field(title="Номер телефона")
    age: int = Field(title="Возраст пользователя")
    password: str = Field(title="Пароль пользователя", max_length=128, min_length=8)
    avatar: Optional[str] = Field(title="Аватар пользователя")
    about_me: Optional[str] = Field(title='Информация об менторе')
    education: Optional[Education] = Field(title="Образование ментора")
    
    class Config:
        orm_mode = True



class MentorExperience(BaseModel):
    position: Optional[str] = Field(title="Должность")
    company: Optional[str] = Field(title="Название компании")
    start_date: Optional[datetime] = Field(title="Дата начала")
    end_date: Optional[datetime] = Field(title="Дата окончания")

    class Config:
        orm_mode = True


class MentorResponseSchema(BaseModel):
    id: int
    name: str = Field(title="Имя ментора")
    last_name: str = Field(title="Фамилия ментора")
    age: int = Field(title="Возраст ментора") 
    phone_number: str = Field(title="Номер телефона")
    education: Optional[Education] = Field(title="Образование")
    avatar: Optional[str] = Field(None, title="Ссылка на аватар")
    experience : Optional[MentorExperience] = Field(None, title='Опыт работы')

    class Config:
        orm_mode = True
        validate_all = True  # Добавьте это, чтобы принудить схему проверять все поля, даже если они необязательные



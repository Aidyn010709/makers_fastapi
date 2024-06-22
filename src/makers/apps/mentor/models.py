from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column, String, DateTime, Enum,
    Integer, Boolean, ForeignKey, Text, ARRAY
)
from makers.apps.db.abstract import UserBase, IDBase
from makers.apps.mentor.constants import Education, EnglishLevel


class Experience(IDBase):

    position = Column(String(128), info={"verbose_name": "Должность"})
    company = Column(String(256), info={"verbose_name": "Название компании"})
    start_date = Column(DateTime(timezone=True), info={"verbose_name": "Дата начала"})
    end_date = Column(DateTime(timezone=True), info={"verbose_name": "Дата окончания"})
    is_present = Column(
        Boolean, default=False, info={"verbose_name": "По настоящее время"}
    )
    mentor_id = Column(Integer, ForeignKey("mentors.id", ondelete="CASCADE"))

    class Meta:
        verbose_name = "Опыт работы"


class Mentor(IDBase, UserBase):
    __tablename__ = 'mentors'

    name = Column(String(100), info={
        "verbose_name": "Имя ментора"
    })
    last_name = Column(String(100), info={
        "verbose_name": "Фамилия ментора"
    })
    age = Column(Integer, info={
        "verbose_name": "Возраст ментора"
    })
    phone_number = Column(String(64), info={
        "verbose_name": "Номер телефона ментора"
    })
    telegram_link = Column(String(128), info={
        "verbose_name": "Ссылка на Телеграмм"
    })
    about_me = Column(Text, info={
        "verbose_name": "О себе"
    })
    education = Column(Enum(Education), info={ # Образование ментора 
        "verbose_name": "Образование"
    })
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), info={
        "verbose_name": "Дата регистрации ментора"
    })
    avatar = Column(Text, info={
        "verbose_name": "Ссылка на аватар"
    })
    english_level = Column(
        Enum(EnglishLevel), info={"verbose_name": "Уровень английского языка"}
    )
    is_active = Column(Boolean, default=True, info={ # по дефолту true потом будет log-out и тогда мы можем сделать false
        "verbose_name": "Активный"
    })
    languages = Column(ARRAY(String), info={"verbose_name": "Языки программировани"})
    
    experience = relationship("Experience", backref="user") # опыт работы ментора просто информация 

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
    Text,
    Enum,
)

from makers.apps.auth.constants import EnglishLevel
from makers.apps.db.abstract import UserBase, IDBase
from makers.apps.mentor.models import Mentor


class User(IDBase, UserBase):
    __tablename__ = "users"

    name = Column(String(100), info={"verbose_name": "Имя пользователя"})
    last_name = Column(String(100), info={"verbose_name": "Фамилия пользователя"})
    phone_number = Column(
        String(64), info={"verbose_name": "Номер телефона пользователя"}
    )
    registered_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        info={"verbose_name": "Дата регистрации пользователя"},
    )
    activation_code = Column(
        String(128), info={"verbose_name": "Активационный код пользователя"}
    )
    is_active = Column(
        Boolean, default=False, info={"verbose_name": "Активный пользователь"}
    )
    is_admin = Column(Boolean, default=False, info={"verbose_name": "Администратор"})
    is_superuser = Column(
        Boolean, default=False, info={"verbose_name": "Супер Администратор"}
    )
    telegram_link = Column(String(128), info={"verbose_name": "Ссылка на Телеграмм"})
    about_me = Column(Text, info={"verbose_name": "О себе"})
    avatar = Column(Text, info={"verbose_name": "Ссылка на аватар"})

    # Новое поле для хранения идентификаторов пользователей, которые поставили лайк данному пользователю
    liked_by = Column(ARRAY(Integer), default=[], info={"verbose_name": "Лайки от пользователей"})

    token = relationship("TokenBlocklist", backref=backref("user"))


    class Meta:
        verbose_name = "Пользователь"

    def __repr__(self):
        return f"Email: {self.email}"
    
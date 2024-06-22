from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, String, BigInteger, DateTime

from makers.apps.db.base_model import Model
from makers.apps.commons.constants import CONSTANTS


class IDBase(Model):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)


class TimestampBase(Model):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now(), index=True, nullable=False)


class UserBase(Model):
    """
    Base attributes
    """

    __abstract__ = True

    email = Column(
        String(255), unique=True, info={"verbose_name": "Почта пользователя"}
    )
    #: Приватный атрибут. Для работы с паролям используется
    #: getter и setter :meth:`.User.password`
    _password = Column(String(128), info={"verbose_name": "Пароль пользователя"})
    #: Пароль в открытом ввиде. Обычный класс атрибут. В таблице нету такого поле
    _password_raw = None

    @hybrid_property
    def password(self) -> str:
        """Возвращает пароль в хэштрованном ввиде.
        :getter: Возвращает строку как есть
        :setter: Перед сохранением хэширует пароль
        """
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        """Перед сохранением в базу хэширует пароль"""
        self._password_raw = value
        self._password = CONSTANTS.PWD_CONTEXT.hash(value)

    def verify_password(self, raw_password):
        """Проверка пароля текущего пользователя

        :param raw_password: Хэширует и сравнимает с записам из базы
        """
        return CONSTANTS.PWD_CONTEXT.verify(raw_password, self._password)

from typing import Callable
from functools import update_wrapper
from abc import ABC, abstractmethod

from loguru import logger

from makers.apps.broker.base import NchanPublisher
from makers.apps.auth.models import User
from makers.config.settings import settings
from makers.apps.events.schemas import EventBase, EventTypes
from makers.apps.commons.constants import get_current_time


class BaseBrokerDecorator(ABC):

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class PublisherWrapper(BaseBrokerDecorator, NchanPublisher):
    """
    Класс обертка для:
    1. Формирования события
    2. Отправки события по Pub/Sub
    """
    def __init__(self, event_type: str = EventTypes.INVITE.value):
        self.func = None
        self.is_published = False
        self.connection_url = settings.PUBLISHER_URL
        self.event_type = event_type
        super().__init__(self.connection_url)

    async def assemble_sign_up_event(self, user: User) -> dict:
        """
        Формирования события для регистрации пользователя
        """
        payload = EventBase(
            user_name=user.name,
            event_type=self.event_type,
            application_id=user.id,
            user_id=user.id,
            created_at=get_current_time()
        )
        return {"payload": payload.dict(), "receiver_id": payload.user_id}

    def __call__(self, func: Callable):
        async def wrapper(*func_args, **func_kwargs):
            update_wrapper(self, func)
            self.func = func
            logger.info(f"Wrapped {self.func.__name__} func")

            # get return value from wrapped function
            user: User = await self.func(*func_args, **func_kwargs)

            # create payload for publish
            payload = await self.assemble_sign_up_event(user)

            # publish payload
            logger.info(f"Payload: {payload}")
            await self.publish(**payload)

            self.is_published = True
            return user

        return wrapper

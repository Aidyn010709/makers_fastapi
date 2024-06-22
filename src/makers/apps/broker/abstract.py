from abc import ABC, abstractmethod


class AbstractPublisher(ABC):
    """
    Abstract class for Publisher
    """

    @abstractmethod
    async def publish(self):
        raise NotImplementedError

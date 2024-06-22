from loguru import logger
from aiohttp import ClientSession
from makers.apps.broker.abstract import AbstractPublisher


class NchanPublisher(AbstractPublisher):
    def __init__(self, connection_url: str):
        self.connection_url = connection_url

    async def publish(self, receiver_id: int, payload: dict):
        logger.info("Start publishing event")
        async with ClientSession() as session:
            url = f"{self.connection_url}?id={receiver_id}"
            async with session.post(url, json=payload, ssl=False) as response:
                payload = await response.text()
                logger.info(f"Response: {payload}")
                logger.info("Event published successfully")

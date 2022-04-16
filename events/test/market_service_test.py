import asyncio

from monitoring.src.logger import Logger
from enums.event_types import EventTypes
from enums.redis_enum import RedisEnums

from events.src.event_manager import EventManager
from storage.redis.src.redis import Redis


class Market_service_test:
    def __init__(self, username):
        self.market_name = ""
        self.market_chanel = self.market_name + RedisEnums.Stream.MARKET
        self.user_data_chanel = self.market_name + RedisEnums.Stream.USER_DATA + username
        self.loop = asyncio.new_event_loop()
        self.logger = Logger(True, '')
        self.event_manager = EventManager(
            market_channel=self.market_chanel,
            user_data_channel=self.user_data_chanel,
            username=username
        )
        self.redis = Redis()
        self.event_manager.start()

    def start(self):
        asyncio.set_event_loop(self.loop)
        asyncio.ensure_future(self.get_orderbook_event())
        self.loop.run_forever()

    async def get_orderbook_event(self):
        self.logger.info("Time to raise orderbook event")
        event = await self.event_manager.get_new_event(
            event_topic=EventTypes.ORDERBOOK_EVENT + "",
            event_type=EventTypes.ORDERBOOK_EVENT,
            loop=self.loop)
        while True:
            await event.wait()
            self.logger.info(event.EVENT_VALUE)
            event.clear()
            await self.event_manager.add_topic_event_into_examiner(event=event)

if __name__ == '__main__':
    ms = Market_service_test(username="TEST")
    ms.start()

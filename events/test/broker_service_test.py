import asyncio
import time
import threading

from monitoring.src.logger import Logger
from enums.redis_enum import RedisEnums
from enums.event_types import EventTypes
from enums.order import Order

from events.src.event_manager import EventManager
from events.src.broker_service import BrokerService
from storage.redis.src.redis import Redis

# logger configuration
TEST_LOGGER = True
TEST_LOGGER_PATH = ""


class BrokerServiceTest:
    def __init__(self, broker_name, username, **kwargs):
        """
        initiating broker test class in order to test events flow on project
        :param broker_name: the broker that the test is going to run on it
        :param username: the user name of account on the broker
        """
        # user and broker configuration
        self.broker_name = broker_name
        self.username = username
        self.send_order_detail = kwargs
        # naming of channels
        self.market_channel = self.broker_name + RedisEnums.Stream.MARKET
        self.user_data_channel = self.broker_name + RedisEnums.Stream.USER_DATA + self.username
        self.user_request_channel = self.broker_name + RedisEnums.Stream.USER_REQUEST + self.username
        # essential objects instances
        self.logger = Logger(TEST_LOGGER, TEST_LOGGER_PATH)
        self.redis = Redis()
        self.loop = asyncio.new_event_loop()
        self.event_manager = EventManager(
            market_channel=self.market_channel,
            user_data_channel=self.user_data_channel,
            username=self.username
        )
        self.broker_service = BrokerService(
            user_request_channel=self.user_request_channel,
            event_manager_obj=self.event_manager,
            loop=self.loop
        )
        # start of event_examiner
        self.event_manager.start()

    def start(self):
        threading.Thread(
            name="start_portfolio_event_test",
            target=self.start_portfolio_event_test,
            daemon=False
        ).start()

    def start_portfolio_event_test(self):
        asyncio.set_event_loop(self.loop)
        asyncio.ensure_future(self.get_portfolio_event())
        self.loop.run_forever()

    async def get_portfolio_event(self):
        self.logger.info("starting portfolio ")
        event = await self.event_manager.get_new_event(
            event_type=EventTypes.ACCOUNT_PORTFOLIO_EVENT,
            event_topic=EventTypes.ACCOUNT_PORTFOLIO_EVENT + "IRT",
            loop=self.loop)
        while True:
            await event.wait()
            self.logger.success(event.EVENT_ID + event.EVENT_TOPIC + str(event.EVENT_VALUE))
            event.clear()

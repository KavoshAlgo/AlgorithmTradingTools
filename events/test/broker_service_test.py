import asyncio
import threading

from monitoring.src.logger import Logger
from enums.redis_enum import RedisEnums
from enums.event_types import EventTypes
from enums.order import Order

from events.src.event_manager import EventManager
from events.src.broker_service import BrokerService
from storage.redis.src.redis import Redis


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
        self.logger = Logger(True, "")
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
        """
        starting tests on destination broker
        creating a thread on portfolio
        and send a test order
        :return:
        """
        threading.Thread(
            name="start_portfolio_event_test",
            target=self.start_user_data_event_test,
            daemon=False
        ).start()
        self.loop.create_task(self.send_test_order_and_cancel())

    def start_user_data_event_test(self):
        asyncio.set_event_loop(self.loop)
        asyncio.ensure_future(self.get_portfolio_event())
        self.loop.run_forever()

    async def get_portfolio_event(self):
        self.logger.info("Starting portfolio event tester")
        event = await self.event_manager.get_new_event(
            event_type=EventTypes.ACCOUNT_PORTFOLIO_EVENT,
            event_topic=EventTypes.ACCOUNT_PORTFOLIO_EVENT + "IRT",
            loop=self.loop)
        while True:
            await event.wait()
            self.logger.success(event.EVENT_TOPIC + ": " + str(event.EVENT_VALUE))
            event.clear()
            await self.event_manager.add_topic_event_into_examiner(event)

    async def send_test_order_and_cancel(self):
        self.logger.info("Trying to send a test order")
        send_order_event = await self.broker_service.send_order(**self.send_order_detail)
        await send_order_event.wait()
        self.logger.success(send_order_event.EVENT_ID + ": " + str(send_order_event.EVENT_VALUE))
        if send_order_event.EVENT_VALUE['status'] == "ok":
            order_id = send_order_event.EVENT_VALUE['response'][Order.ORDER_ID]
            await asyncio.sleep(2)
            self.logger.info("Trying to cancel the order")
            cancel_order_event = await self.broker_service.cancel_order(order_id=order_id)
            await cancel_order_event.wait()
            self.logger.success(cancel_order_event.EVENT_TOPIC + ": " + str(send_order_event.EVENT_VALUE))
        else:
            self.logger.error(send_order_event.EVENT_VALUE['response'])

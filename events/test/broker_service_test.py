import asyncio

from monitoring.src.logger import Logger
from enums.redis_enum import RedisEnums
from enums.event_types import EventTypes
from enums.order import Order

from events.src.event_manager import EventManager
from events.src.broker_service import BrokerService
from storage.redis.src.redis import Redis


class BrokerServiceTest:
    def __init__(self, broker_name, username, test_scenario, **kwargs):
        """
        initiating broker test class in order to test events flow on project
        :param broker_name: the broker that the test is going to run on it
        :param username: the username of account on the broker
        """
        # user and broker configuration
        self.broker_name = broker_name
        self.username = username
        self.test_scenario = test_scenario
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
        asyncio.set_event_loop(self.loop)
        asyncio.ensure_future(self.get_portfolio_event())
        self.loop.create_task(self.test_executor())
        self.loop.run_forever()

    async def get_portfolio_event(self):
        """
        detect changes on ACCOUNT_PORTFOLIO_EVENT
        :return:
        """
        self.logger.info("Starting portfolio event notifier")
        event = await self.event_manager.get_new_event(
            event_type=EventTypes.ACCOUNT_PORTFOLIO_EVENT,
            event_topic=EventTypes.ACCOUNT_PORTFOLIO_EVENT + "IRT",
            loop=self.loop)
        while True:
            await event.wait()
            self.logger.success(event.EVENT_TOPIC + ": " + str(event.EVENT_VALUE))
            event.clear()
            await self.event_manager.add_topic_event_into_examiner(event)

    async def get_order_event(self, order_id):
        """
        detect changes on ACCOUNT_ORDER_EVENT
        :return:
        """
        self.logger.info("Starting order event notifier")
        event = await self.event_manager.get_new_event(
            event_type=EventTypes.ACCOUNT_ORDER_EVENT,
            event_topic=EventTypes.ACCOUNT_ORDER_EVENT + str(order_id),
            loop=self.loop)
        while True:
            await event.wait()
            self.logger.success(event.EVENT_TOPIC + ": " + str(event.EVENT_VALUE))
            event.clear()
            await self.event_manager.add_topic_event_into_examiner(event)

    async def test_executor(self):
        """
        executing the incoming test scenarios.
        :return:
        """
        self.logger.info("Trying to send a test order")
        send_order_event = await self.broker_service.send_order(**self.send_order_detail)
        await send_order_event.wait()
        self.logger.success(send_order_event.EVENT_ID + ": " + str(send_order_event.EVENT_VALUE))
        if self.test_scenario == "order":
            if send_order_event.EVENT_VALUE['status'] == "ok":
                order_id = send_order_event.EVENT_VALUE['response'][Order.ORDER_ID]
                asyncio.ensure_future(self.get_order_event(order_id))
                await asyncio.sleep(5)
                self.logger.info("Trying to cancel the order")
                cancel_order_event = await self.broker_service.cancel_order(order_id=order_id)
                await cancel_order_event.wait()
                self.logger.success(cancel_order_event.EVENT_TOPIC + ": " + str(send_order_event.EVENT_VALUE))
            else:
                self.logger.error(send_order_event.EVENT_VALUE['response'])
        elif self.test_scenario == "trade":
            if send_order_event.EVENT_VALUE['status'] == "ok":
                order_id = send_order_event.EVENT_VALUE['response'][Order.ORDER_ID]
                asyncio.ensure_future(self.get_order_event(order_id))
            else:
                self.logger.error(send_order_event.EVENT_VALUE['response'])


if __name__ == '__main__':
    """ 
    in this section we need to determine what kind of test scenario we are going to run.
    the available scenarios are :
    [send_test_order_and_cancel: order, send_test_order_and_trade: trade]
    no matter what we choose the test runner is going to notice the changes on 
    portfolio and order status changes.
    NOTICE : ** please consider in order to run the trade test u need to place a possible to trade order **
    """
    bst = BrokerServiceTest(
        broker_name="",
        username="",
        test_scenario="order",
        **{
            Order.MARKET: "USDTIRT",
            Order.SIDE: Order.OrderSide.BUY,
            Order.PRICE: 277000,
            Order.VOLUME: 15
        }
    )
    bst.start()

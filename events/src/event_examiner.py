import asyncio
import threading

from streaming.src.stream_consumer import StreamConsumer
from events.src.event import Event
from enums.orderbooks import Orderbooks
from enums.event_types import EventTypes
from enums.order import Order
from enums.algorithm_request import AlgorithmRequest
from enums.portfolio import Portfolio


class EventExaminer:
    def __init__(self, market_channel, user_data_channel, username):
        self.market_channel_consumer = StreamConsumer(market_channel)
        self.user_data_channel_consumer = StreamConsumer(user_data_channel)
        self.username = username
        self.topics_events = dict()
        self.cache_orders = dict()
        self.lock = asyncio.Lock()
        self.user_data_channel_loop = None
        self.market_channel_loop = None

    def start(self):
        threading.Thread(
            name="examine_user_data_channel_loop",
            target=self.create_user_data_channel_loop,
            daemon=False
        ).start()
        threading.Thread(
            name="examine_market_channel_loop",
            target=self.create_market_channel_loop,
            daemon=False
        ).start()

    def create_user_data_channel_loop(self):
        self.user_data_channel_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.user_data_channel_loop)
        asyncio.ensure_future(self.examine_user_data_channel_events())
        self.user_data_channel_loop.run_forever()

    def create_market_channel_loop(self):
        self.market_channel_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.market_channel_loop)
        asyncio.ensure_future(self.examine_market_channel_events())
        self.market_channel_loop.run_forever()

    async def examine_market_channel_events(self):
        while True:
            data = self.market_channel_consumer.consume()
            for item in data:
                topic = item[AlgorithmRequest.EVENT_TYPE] + item[Orderbooks.MARKET]
                if topic in self.topics_events:
                    events = self.topics_events[topic]
                    await self.trigger_topics_events(events, item)
                else:
                    # print("Missed Event in examine_events_market_channel")
                    pass

    async def examine_user_data_channel_events(self):
        while True:
            data = self.user_data_channel_consumer.consume()
            for item in data:
                topic = None
                if item[AlgorithmRequest.EVENT_TYPE] == EventTypes.ACCOUNT_ORDER_EVENT:
                    topic = item[AlgorithmRequest.EVENT_TYPE] + str(item[Order.ORDER_ID])
                elif item[AlgorithmRequest.EVENT_TYPE] == EventTypes.ACCOUNT_PORTFOLIO_EVENT:
                    topic = item[AlgorithmRequest.EVENT_TYPE] + item[Portfolio.SYMBOL]
                elif item[AlgorithmRequest.EVENT_TYPE] == EventTypes.ALGORITHM_REQUEST_EVENT:
                    topic = item[AlgorithmRequest.EVENT_TYPE] + str(item[AlgorithmRequest.JOB_ID])

                if topic and topic in self.topics_events:
                    events = self.topics_events[topic]
                    await self.trigger_topics_events(events, item)
                else:
                    # print("Missed Event in examine_events_account_data_channel")
                    if EventTypes.ACCOUNT_ORDER_EVENT in topic:
                        self.cache_orders[topic] = item

    async def add_topic_event(self, event: Event):
        async with self.lock:
            if event.EVENT_TOPIC in self.topics_events.keys():
                self.topics_events[event.EVENT_TOPIC].append(event)
            else:
                if event.EVENT_TOPIC in self.cache_orders:
                    await self.trigger_topics_events([event], self.cache_orders[event.EVENT_TOPIC])
                    self.cache_orders.pop(event.EVENT_TOPIC)
                else:
                    self.topics_events[event.EVENT_TOPIC] = [event]

    @staticmethod
    async def trigger_topics_events(events, value):
        for event in events:
            event.trigger_event(value)

    async def remove_topic_events(self, topic):
        async with self.lock:
            events = self.topics_events.pop(topic)
            return events

import asyncio
import threading

from streaming.src.stream_consumer import StreamConsumer
from events.event import Event
from enums.orderbooks import Orderbooks
from enums.event_types import EventTypes
from enums.order import Order
from enums.algorithm_request import AlgorithmRequest


class EventExaminer:
    def __init__(self, market_channel_name, account_data_channel_name, account_username):
        self.market_channel_consumer = StreamConsumer(market_channel_name)
        self.account_data_channel_consumer = StreamConsumer(account_data_channel_name)
        self.account_username = account_username
        self.topics_events = dict()
        self.lock = asyncio.Lock()
        self.loop = None
        self.loop2 = None

    def start(self):
        threading.Thread(name="examine_events_account_data_channel_loop", target=self.create_loop, daemon=False).start()
        threading.Thread(name="examine_events_market_channel_loop", target=self.create_loop2, daemon=False).start()

    def create_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        asyncio.ensure_future(self.examine_events_account_data_channel())
        self.loop.run_forever()

    def create_loop2(self):
        self.loop2 = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop2)
        asyncio.ensure_future(self.examine_events_market_channel())
        self.loop2.run_forever()

    async def examine_events_market_channel(self):
        while True:
            data = self.market_channel_consumer.consume()
            for item in data:
                topic = item[AlgorithmRequest.EVENT_TYPE] + item[Orderbooks.MARKET]
                if topic in self.topics_events:
                    events = await self.remove_topic_events(topic)
                    await self.trigger_topics_events(events, item)
                else:
                    print("Missed Event in examine_events_market_channel")

    async def examine_events_account_data_channel(self):
        while True:
            data = self.account_data_channel_consumer.consume()
            for item in data:
                topic = None
                if item[AlgorithmRequest.EVENT_TYPE] == EventTypes.ACCOUNT_ORDER_EVENT:
                    topic = item[AlgorithmRequest.EVENT_TYPE] + str(item[Order.ORDER_ID])
                elif item[AlgorithmRequest.EVENT_TYPE] == EventTypes.ACCOUNT_PORTFOLIO_EVENT:
                    topic = item[AlgorithmRequest.EVENT_TYPE] + self.account_username
                elif item[AlgorithmRequest.EVENT_TYPE] == EventTypes.ALGORITHM_REQUEST_EVENT:
                    topic = item[AlgorithmRequest.EVENT_TYPE] + str(item[AlgorithmRequest.JOB_ID])

                if topic and topic in self.topics_events:
                    events = await self.remove_topic_events(topic)
                    await self.trigger_topics_events(events, item)
                else:
                    print("Missed Event in examine_events_account_data_channel")

    async def add_topic_event(self, event: Event):
        async with self.lock:
            if event.EVENT_TOPIC in self.topics_events.keys():
                self.topics_events[event.EVENT_TOPIC].append(event)
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

    # TODO: ignore these two functions for now
    def tag_orders_on_orderbook(self):
        pass

    def update_active_orders(self):
        pass


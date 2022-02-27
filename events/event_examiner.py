import asyncio
import threading

from streaming.src.stream_consumer import StreamConsumer
from events.event import Event
from enums.orderbooks import Orderbooks
from enums.event_types import EventTypes


class EventExaminer:
    def __init__(self, market_channel_name, account_data_channel_name, account_username):
        self.market_channel_consumer = StreamConsumer(market_channel_name)
        self.account_data_channel_consumer = StreamConsumer(account_data_channel_name)
        self.account_username = account_username
        self.topics_events = dict()
        self.lock = asyncio.Lock()
        self.loop = None

    def start(self):
        threading.Thread(name="EventExaminer_loop", target=self.create_loop, daemon=False).start()

    def create_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        asyncio.ensure_future(self.examine_events_market_channel())
        asyncio.ensure_future(self.examine_events_account_data_channel())
        self.loop.run_forever()

    async def examine_events_market_channel(self):
        while True:
            data = self.market_channel_consumer.consume()
            for item in data:
                topic = item["event_type"] + item[Orderbooks.MARKET]
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
                if item["event_type"] == EventTypes.ACCOUNT_ORDER_EVENT:
                    topic = item["event_type"] + str(item[Orderbooks.ID])
                elif item["event_type"] == EventTypes.ACCOUNT_PORTFOLIO_EVENT:
                    topic = item["event_type"] + self.account_username
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

    async def trigger_topics_events(self, events, value):
        for event in events:
            event.trigger_event(value)

    async def remove_topic_events(self, topic):
        async with self.lock:
            events = self.topics_events[topic].pop()
            return events

    # TODO: ignore these two functions for now
    def tag_orders_on_orderbook(self):
        pass

    def update_active_orders(self):
        pass


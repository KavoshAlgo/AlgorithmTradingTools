import asyncio


class Event(asyncio.Event):
    EVENT_TYPE: str
    EVENT_VALUE: dict
    EVENT_ID: str
    EVENT_TOPIC: str

    def __init__(self, event_id, event_type,  event_topic):
        self.EVENT_ID = event_id
        self.EVENT_TOPIC = event_topic
        self.EVENT_TYPE = event_type

    def trigger_event(self, value):
        self.EVENT_VALUE = value
        self.set()

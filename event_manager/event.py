import asyncio


class Event(asyncio.Event):
    EVENT_TYPE: str
    EVENT_VALUE: dict
    EVENT_ID: str
    EVENT_TOPIC: str

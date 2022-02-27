import random
import string
import time

from monitoring.src.logger import Logger

from events.config import EventManagerConfig
from events.event_examiner import EventExaminer
from events.event import Event


class EventManager:
    def __init__(self):
        self.event_examiner = EventExaminer()
        self.logger = Logger(False, '')

    def start(self):
        self.event_examiner.start()

    async def get_new_event(self, event_type: str, event_topic: str, event_id=None) -> Event:
        if not event_id:
            event_id = self.generate_event_id()
        event = Event(event_id=event_id, event_type=event_type, event_topic=event_topic)
        await self.add_topic_event_into_examiner(event)
        return event

    @staticmethod
    def generate_event_id() -> str:
        hash_string_id = ''.join(random.choices(string.ascii_lowercase, k=EventManagerConfig.ID_HASH_STRING_LENGTH))
        timestamp = str(int(time.time() * (10 ** 6)))
        return timestamp + "_" + hash_string_id

    async def add_topic_event_into_examiner(self, event: Event):
        await self.event_examiner.add_topic_event(event)

import random
import string
import time

from monitoring.src.logger import Logger

from event_manager.config import EventManagerConfig
from event_manager.event_examiner import EventExaminer
from event_manager.event import Event


class EventManager:
    def __init__(self):
        self.event_examiner = EventExaminer()
        self.logger = Logger(False, '')

    def start(self):
        self.event_examiner.start()

    def get_new_event(self, topic : str) -> Event:
        event = Event(event_id=self.generate_event_id(),  event_topic=topic)
        self.add_topic_event_into_examiner(event)
        return event

    @staticmethod
    def generate_event_id() -> str:
        hash_string_id = ''.join(random.choices(string.ascii_lowercase, k=EventManagerConfig.ID_HASH_STRING_LENGTH))
        timestamp = str(int(time.time() * (10 ** 6)))
        return timestamp + "_" + hash_string_id

    def add_topic_event_into_examiner(self, event: Event):
        if event.EVENT_TOPIC in self.event_examiner.topics_events:
            self.event_examiner.topics_events[event.EVENT_TOPIC].append(event.EVENT_ID)
        else:
            self.event_examiner.topics_events[event.EVENT_TOPIC] = [event.EVENT_ID]


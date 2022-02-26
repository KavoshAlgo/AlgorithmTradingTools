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

    def get_new_event(self):
        return Event(self.generate_event_id())

    @staticmethod
    def generate_event_id():
        hash_string_id = ''.join(random.choices(string.ascii_lowercase, k=EventManagerConfig.ID_HASH_STRING_LENGTH))
        timestamp = str(int(time.time() * (10 ** 6)))
        return timestamp + "_" + hash_string_id

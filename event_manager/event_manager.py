from event_manager.event_examiner import EventExaminer
from monitoring.src.logger import Logger


class EventManager:
    def __init__(self):
        self.event_examiner = EventExaminer()
        self.logger = Logger(False, '')
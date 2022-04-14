from monitoring.src.logger import Logger
from enums.redis_enum import RedisEnums

from events.src.event_manager import EventManager
from streaming.src.stream_producer import StreamProducer
from streaming.src.stream_consumer import StreamConsumer
from streaming.src.algorithm_operations import AlgorithmOperations

# logger configuration
TEST_LOGGER = True
TEST_LOGGER_PATH = ""
# user configuration
BROKER_NAME = ""
USERNAME = " "

MARKET_CHANNEL = BROKER_NAME + RedisEnums.Stream.MARKET
USER_DATA_CHANNEL = BROKER_NAME + RedisEnums.Stream.USER_DATA + USERNAME
USER_REQUEST_CHANNEL = BROKER_NAME + RedisEnums.Stream.USER_REQUEST + USERNAME


class BrokerServiceTest:
    def __init__(self):
        self.logger = Logger(TEST_LOGGER, TEST_LOGGER_PATH)
        self.event_manager = EventManager(MARKET_CHANNEL, USER_DATA_CHANNEL, USERNAME)


if __name__ == '__main__':
    bst = BrokerServiceTest()

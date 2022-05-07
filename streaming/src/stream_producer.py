import json
import redis

from monitoring.src.logger import Logger
from streaming.config import StreamConfig


class StreamProducer:

    def __init__(self):
        """
        create an object of the RedisProducer
        """
        self.logger = Logger(
            main=StreamConfig.PRODUCER_LOGGER,
            file_name=StreamConfig.PRODUCER_LOGGER_PATH
        )
        self.redis_connection = redis.Redis(
            host=StreamConfig.REDIS_SERVER,
            port=StreamConfig.REDIS_PORT,
            password=StreamConfig.REDIS_PASSWORD)
        self.logger.info("create a connection to Redis Server as a producer ....")
        self.logger.info("producer connection is established")

    def send(self, topic, message, maxlen=None):
        self.redis_connection.xadd(
            topic,
            {"data": json.dumps(message)},
            maxlen=maxlen
        )


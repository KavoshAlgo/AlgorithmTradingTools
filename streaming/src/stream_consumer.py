import json
import redis
import aioredis
import time

from monitoring.src.logger import Logger
from streaming.config import StreamConfig
from enums.streams import ReceiveMode


class StreamConsumer:
    def __init__(self, topic, receive_mode=ReceiveMode.ALL):
        """
        create a connection to the kafka stream channel and consume the channel
        :param topic:  the topic of stream channel in Redis
        :param receive_mode:  "all" or "latest", when config mode on all we consume all data on
            the stream but when set this config on latest we consume the latest one
        :return an object with a consumer attribute
        """
        self.logger = Logger(
            main=StreamConfig.CONSUMER_LOGGER,
            file_name=StreamConfig.CONSUMER_LOGGER_PATH
        )
        self.topic = topic
        self.receive_mode = receive_mode
        if self.receive_mode == ReceiveMode.ALL:
            self.id_dict = {self.topic: bytes("%s-0" % int(time.time() * 1000), "utf-8")}
        elif self.receive_mode == ReceiveMode.LATEST:
            self.id_dict = {self.topic: bytes("$", "utf-8")}
        self.logger.info("create a connection to redis channel as a consumer ....")
        # self.redis_connection = redis.Redis(
        #     host=StreamConfig.REDIS_SERVER,
        #     port=StreamConfig.REDIS_PORT,
        #     password=StreamConfig.REDIS_PASSWORD)
        self.redis_connection = aioredis.from_url(
            StreamConfig.REDIS_SERVER,
            port=StreamConfig.REDIS_PORT,
            password=StreamConfig.REDIS_PASSWORD
        )
        self.logger.info("consumer connection is established")

    async def consume(self):
        data = await self.redis_connection.xread(
            self.id_dict,
            StreamConfig.MAX_EVENTS_COUNT,
            block=StreamConfig.CONSUMER_BLOCK_TIMEOUT
        )
        if len(data) > 0:
            self.id_dict = {self.topic: list(data[0][1][-1])[0]}
            events = []
            for i in range(len(list(data[0][1]))):
                events.append(json.loads(list(data[0][1][i])[1][b"data"]))
            return events

import json

from monitoring.src.logger import Logger
from streaming.config import StreamConfig
from kafka import KafkaConsumer


class StreamConsumer:
    def __init__(self, topic, **args):
        """
        create a connection to the kafka stream channel and consume the channel
        :param client_id:  the client id of consumer
        :param topic:  the topic of stream channel in Kafka
        :param timeout:  the timeout of stream connection for receiving data
        :param auto_offset_reset:  "earliest" or "latest", start from last offset we consume or the latest one, Default:
         "earliest"
        :return an object with a consumer attribute
        """
        self.logger = Logger(
            main=StreamConfig.CONSUMER_LOGGER,
            file_name=StreamConfig.CONSUMER_LOGGER_PATH
        )
        args["value_deserializer"] = lambda m: json.loads(m.decode('ascii'))
        self.logger.info("create a connection to kafka channel(%s) as a consumer ...." % topic)
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[StreamConfig.KAFKA_SERVER],
            **args
        )
        self.logger.info("%s consumer connection is established" % topic)

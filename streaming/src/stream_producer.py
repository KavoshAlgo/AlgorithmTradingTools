import json

from monitoring.src.logger import Logger
from streaming.config import StreamConfig
from kafka import KafkaProducer


class StreamProducer:

    def __init__(self, **kwargs):
        """
        create an object of the KafkaProducer
        :param client_id: the client id of the producer
        :param timeout: timeout of the sending message to the channel
        """
        self.logger = Logger(
            main=StreamConfig.PRODUCER_LOGGER,
            file_name=StreamConfig.PRODUCER_LOGGER_PATH
        )
        kwargs['value_serializer'] = lambda m: json.dumps(m).encode('ascii')
        kwargs['bootstrap_servers'] = [StreamConfig.KAFKA_SERVER]
        self.logger.info("create a connection to kafka as a producer ....")
        self.producer = KafkaProducer(**kwargs)
        self.logger.info("producer connection is established")

    def send(self, topic, message):
        self.producer.send(topic, message).add_callback(self.on_send_success).add_callback(self.on_send_error)

    def on_send_success(self, record_metadata):
        self.logger.info(record_metadata.topic)
        self.logger.info(record_metadata.partition)

    def on_send_error(self, error):
        self.logger.error('sending msg to the kafka face an error: %s' % error)

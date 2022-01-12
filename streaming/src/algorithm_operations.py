import threading
import random
import string

from streaming.src.stream_consumer import StreamConsumer
from streaming.src.stream_producer import StreamProducer
from streaming.config import StreamConfig

from monitoring.src.logger import Logger


class AlgorithmOperations:
    def __init__(self, operation_producer: StreamProducer, user_data_consumer: StreamConsumer, producer_topic: str):
        """
        create an object of the AlgorithmOperations that handle communication with broker side
        :rtype: AlgorithmOperations object
        :param operation_producer: the producer instance
        :param user_data_consumer: the consumer instance
        :param producer_topic: the consumer stream channel
        """
        self.operation_producer = operation_producer
        self.user_data_consumer = user_data_consumer

        self.producer_topic = producer_topic
        '''
            handle jobs with this dictionary
        '''
        self.jobs = {}
        self.logger = Logger(StreamConfig.ALGORITHM_OPERATION_LOGGER, StreamConfig.ALGORITHM_OPERATION_LOGGER_PATH)

    def start(self):
        try:
            threading.Thread(name="start_consume_user_data", target=self.consume, daemon=False).start()
        except Exception as ex:
            self.logger.error("Could not start the consume_user_data thread :" + str(ex))

    def consume(self):
        while True:
            results = self.user_data_consumer.consume()
            for item in results:
                if "job" in item:
                    self.jobs[item["job_id"]] = item

    def send_order(self, **kwargs):
        return self.do_job("send_order", **kwargs)

    def cancel_order(self, **kwargs):
        return self.do_job("cancel_order", **kwargs)

    def do_job(self, job, **kwargs):
        job_id = self.generate_id()
        self.operation_producer.send(self.producer_topic, {
            "job_id": job_id,
            "job": job,
            "job_args": kwargs
        })
        while True:
            if job_id in self.jobs:
                return self.jobs[job_id]["response"], self.jobs[job_id]["status"]

    @staticmethod
    def generate_id():
        job_id = ''.join(random.choices(string.ascii_lowercase, k=StreamConfig.ID_HASH_STRING_LENGTH))
        return job_id

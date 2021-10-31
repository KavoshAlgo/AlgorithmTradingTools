import unittest
import json

from storage.src.queue import QueueConsumer, QueueProducer
from configuration.credentials import QUEUE_HOST


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queueProducer = QueueProducer(host=QUEUE_HOST)
        self.one = {'one': 'one'}
        self.two = {'two': 'two'}

    def test_create_queue(self):
        self.queueProducer.create_queue("test_queue")
        self.queueProducer.produce("test_queue", self.one)
        self.queueProducer.produce("test_queue", self.two)
        consumer = Consumer(self.one, self.two)
        consumer.start_consume("test_queue")

    def test_create_priority_queue(self):
        self.queueProducer.create_priority_queue("priority_queue", 2)
        self.queueProducer.produce("priority_queue", self.two, 0)
        self.queueProducer.produce("priority_queue", self.one, 1)
        consumer = Consumer(self.one, self.two)
        consumer.start_consume("priority_queue")

    def assert_dicts_equal(self, first, second):
        self.assertDictEqual(first, second)


class Consumer(QueueConsumer):
    def __init__(self, first_record, second_record):
        super().__init__(host=QUEUE_HOST)
        self.first_record = first_record
        self.second_record = second_record
        self.consume_counter = 0

    def consume(self, channel, method, properties, body):
        dict_str = body.decode("UTF -8")
        test_queue = TestQueue()
        if self.consume_counter == 0:
            self.consume_counter += 1
            test_queue.assert_dicts_equal(json.loads(dict_str),  self.first_record)
        else:
            test_queue.assert_dicts_equal(json.loads(dict_str), self.second_record)
            self.stop_consume()


if __name__ == '__main__':
    unittest.main()

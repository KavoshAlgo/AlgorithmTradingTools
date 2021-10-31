from abc import abstractmethod, ABC

import pika
import json


class Queue:
    def __init__(self, host='localhost'):
        """
        initialize Rabbitmq connection and channel for QueueClass
        
        :param host: address of the rabbitmq service connection
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def create_queue(self, queue_name):
        """
        create queue without priorty on rabbitmq

        :param queue_name: Name of the Queue
        """
        self.channel.queue_declare(queue=queue_name)

    def create_priority_queue(self, queue_name, max_priority: int):
        """
        create queue with priorty on rabbitmq

        :param queue_name: Name of the Queue
        :param max_priority: set priority of the queue
        """
        self.channel.queue_declare(queue=queue_name, arguments={'x-max-priority': max_priority})


class QueueConsumer(Queue, ABC):
    def __init__(self, host='localhost'):
        """
        initialize Rabbitmq connection and channel for ConsumeQueueClass,
        ConsumeQueue class calling __init__ of Queue(Parent) class

        :param host: address of the rabbitmq service connection
        """
        super().__init__(host)

    def start_consume(self, queue_name):
        """
        start the consume on the rabbitmq queue with callback function

        :param queue_name: Name of the Queue
        :param consume: callback function consume
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.consume, auto_ack=True)
        self.channel.start_consuming()

    def stop_consume(self):
        self.channel.stop_consuming()

    @abstractmethod
    def consume(self, channel, method, properties, body):
        """
        This is a callback function for consuming from rabbitmq Queues

        :param channel: channel of rabbitmq connenction
        :param method: method 
        :param properties: properties of the item in the Queue
        :param body: body of the item in the Queue
        """
        pass


class QueueProducer(Queue):
    def __init__(self, host='localhost'):
        """
        initialize Rabbitmq connection and channel for ProduceQueueClass,
        ProduceQueue class calling __init__ of Queue(Parent) class

        :param host: address of the rabbitmq service connection
        """
        super().__init__(host)

    def produce(self, queue_name, content, priority=None):
        """
        Publish content into a queue

        :param queue_name: Name of the Queue
        :param content: content of the Queue
        :param priority: priority of the Queue
        """
        if priority:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                properties=pika.BasicProperties(
                    priority=priority),
                body=json.dumps(content)
            )
        else:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(content)
            )

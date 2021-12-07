import redis
import json


class Redis:
    def __init__(self, password, host="localhost", port=6379):
        self.redis_connection = redis.Redis(
            host=host,
            port=port,
            password=password
        )

    def insert_hash_set_record(self, hash_set_name, id, content):
        """
        insert a new record into a redis hash set.
        :param hash_set_name: name of the redis hash set
        :param id: id of the content in the hash set
        :param content: the value that is mapped with id

        If there is a problem in setting the record, the function raise an Exception.
        """
        self.redis_connection.hset(
            name=hash_set_name,
            key=id,
            value=json.dumps(content)
        )

    def insert_set_record(self, set_name, content, expiration_time=None):
        """
        insert a new record into a redis set.
        :param set_name: name of the redis set
        :param content: the value is saved into redis set
        :param expiration_time: if it is set after this time, the content will be expired by the redis

        If there is a problem in setting the record, the function raise an Exception.
        """
        if expiration_time:
            self.redis_connection.setex(
                name=set_name,
                value=json.dumps(content),
                time=expiration_time
            )
        else:
            self.redis_connection.set(
                name=set_name,
                value=json.dumps(content)
            )

    def update_hash_set_record(self, hash_set_name, id, content):
        """
        update a record in the redis hash set
        :param hash_set_name: name of the redis hash set
        :param id: id of the content in the hash set
        :param content: the value that is mapped with id

        If there is a problem in setting the record, the function raise an Exception.
        """
        self.insert_hash_set_record(
            hash_set_name=hash_set_name,
            id=id,
            content=content
        )

    def delete_hash_set_record(self, hash_set_name, id):
        """

        :param hash_set_name: the name of redis hash set
        :param id: id in the hash set that we want to delete it
        """
        self.redis_connection.hdel(
            hash_set_name,
            id
        )

    def check_hash_set_record(self, hash_set_name, id):
        """
        check if an id exists in hash-set or not.
        :param hash_set_name: the name of redis hash set
        :param id: id in the hash set that we want to check it
        :return:
        """
        return self.redis_connection.hexists(hash_set_name, id)

    def get_hash_set_record(self, hash_set_name, id):
        """

        :param hash_set_name: the name of redis hash set that we want
        :param id: the key of the value that we want
        :return: The value of this key in the redis hash set
        """
        temp = self.redis_connection.hget(name=hash_set_name, key=id)
        if temp:
            return json.loads(temp)
        else:
            return None

    def get_set_record(self, set_name):
        """

        :param set_name: the name of redis set that we want
        :return: The value of the redis set
        """
        temp = self.redis_connection.get(name=set_name)
        if temp:
            return json.loads(temp)
        else:
            return None

    def get_all_hash_set_records(self, hash_set_name):
        """

        :param hash_set_name: name of the hash set
        :return: all of the hash set content
        """
        temp = self.redis_connection.hgetall(hash_set_name)
        temp_dic = {json.loads(key): json.loads(value) for key, value in temp.items()}
        if temp:
            return temp_dic
        else:
            return None

    def push_to_queue(self, queue_name, item):
        """
        pushing and storing data into redis lists from right.

        :param queue_name: name of the queue
        :param item: the value that is going to saved into queue
        :return:
        """
        self.redis_connection.rpush(queue_name, json.dumps(item))

    def pop_from_queue(self, queue_name):
        """
        popping and removing data from redis lists from left.

        :param queue_name: name of the queue
        :return:
        """
        temp = self.redis_connection.lpop(queue_name)
        if temp is not None:
            return json.loads(temp)
        else:
            return temp

import redis
import json

from storage.config import REDIS_PASSWORD, REDIS_PORT, REDIS_HOST


class Redis:
    def __init__(self, password=REDIS_PASSWORD, host=REDIS_HOST, port=REDIS_PORT):
        self.redis_connection = redis.Redis(
            host=host,
            port=port,
            password=password)

    def insert_sorted_set_record(self, sorted_set_name, dicti):
        """
        insert a new record into a redis sorted set.
        :param sorted_set_name: name of the redis sorted set
        :param dict: format:{name:score}
        :return: returns the cardinality of the named sorted set
        """
        self.redis_connection.zadd(name=sorted_set_name, mapping=dicti)
        return self.redis_connection.zcard(sorted_set_name)

    def get_all_sorted_set_record(self, sorted_set_name, desc=True):
        """
        get the sorted set in an ascending order or in an descending order
        :param sorted_set_name: name of the redis sorted set
        :param desc: flag for the order type
        :return: list of keys in byte string format or None
        """
        temp = self.redis_connection.zrange(sorted_set_name, 0, -1, desc=desc)

        if temp:
            return temp
        else:
            return None

    def get_ranged_sorted_set_count(self, sorted_set_name, mini, maxi):
        """
        get the sorted set in a specified range
        :param sorted_set_name: name of the redis sorted set
        :param mini: minimum of the range
        :param maxi: maximum of the range
        :return: item count or 0 for not found
        """
        temp = self.redis_connection.zcount(sorted_set_name, mini, maxi)

        if temp:
            return temp
        else:
            return 0

    def get_sorted_set_score_record(self, sorted_set_name, key):
        """
        get the score of a record in the sorted set
        :param sorted_set_name: name of the redis sorted set
        :param key: name of the record
        :return: score of the requested record or None
        """
        temp = self.redis_connection.zscore(sorted_set_name, key)

        if temp:
            return temp
        else:
            return None

    def get_ranged_sorted_set_score(self, sorted_set_name, mini, maxi, withscores=True):
        """
        get the records in a specified range with their scores
        :param sorted_set_name: name of the redis sorted set
        :param mini: minimum of the range
        :param maxi: maximum of the range
        :param withscores: flag for showing the scores or not
        :return: list of keys with their scores or None
        """
        temp = self.redis_connection.zrangebyscore(sorted_set_name, min=mini, max=maxi, withscores=withscores)

        if temp:
            return temp
        else:
            return None

    def get_ranged_sorted_set_score_reversed(self, sorted_set_name, mini, maxi, withscores=True):
        """
        get the records in a specified range with their scores reversed
        :param sorted_set_name: name of the redis sorted set
        :param mini: minimum of the range
        :param maxi: maximum of the range
        :param withscores: flag for showing the scores or not
        :return: list of keys with their scores or None
        """
        temp = self.redis_connection.zrevrangebyscore(sorted_set_name, min=mini, max=maxi, withscores=withscores)

        if temp:
            return temp
        else:
            return None

    def remove_sorted_set_record_by_key(self, sorted_set_name, *value):
        """
        remove record(s) by its/their key
        :param sorted_set_name: name of the redis sorted set
        :param value: keys to be removed
        :return: count of the removed items or None
        """
        temp = self.redis_connection.zrem(sorted_set_name, *value)

        if temp:
            return temp
        else:
            return None

    def remove_sorted_set_record_by_ranged_score(self, sorted_set_name, mini, maxi):
        """
        remove record(s) by its/their scores in a specified range
        :param sorted_set_name: name of the redis sorted set
        :param mini: minimum of the range
        :param maxi: maximum of the range
        :return: count of the removed items or None
        """
        temp = self.redis_connection.zremrangebyscore(sorted_set_name, mini, maxi)

        if temp:
            return temp
        else:
            return None

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
        temp_dic = {key.decode("utf-8"): json.loads(value) for key, value in temp.items()}
        if temp:
            return temp_dic
        else:
            return None

    def push_to_queue(self, queue_name: str, item: dict) -> None:
        """
        pushing and storing data into redis lists from right.

        :param queue_name: name of the queue
        :param item: the value that is going to saved into queue
        :return:
        """
        self.redis_connection.rpush(queue_name, json.dumps(item))

    def pop_from_queue(self, queue_name: str, timeout: int = 0) -> dict or None:
        """
        popping and removing data from redis lists from left.

        @param queue_name: name of the queue
        @param timeout: the amount of time the procedure must wait for incoming data on the queue
        :return: the data
        """
        temp = self.redis_connection.blpop(queue_name, timeout=timeout)
        if temp:
            return json.loads(temp[1])
        return temp

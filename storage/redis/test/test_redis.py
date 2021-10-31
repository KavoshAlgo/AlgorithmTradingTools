import unittest

from storage.src.redis import Redis
from configuration.credentials import REDIS_PASSWORD, REDIS_HOST, REDIS_PORT


class TestRedis(unittest.TestCase):
    def setUp(self):
        self.redis = Redis(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT)

        self.set = {"set": "set"}
        self.set_name = "test_set"

        self.hset = {"hset": "hset"}
        self.hset_update = {"hset_update": "hset_update"}
        self.hset_name = "test_hset"
        self.hset_id = "test_hset"

    def test_insert_hash_set_record(self):
        self.redis.insert_hash_set_record(self.hset_name, self.hset_id, self.hset)
        self.assertDictEqual(self.hset, self.redis.get_hash_set_record(self.hset_name, self.hset_id))

    def test_insert_set_record(self):
        self.redis.insert_set_record(self.set_name, self.set)
        self.assertDictEqual(self.set, self.redis.get_set_record(self.set_name))

    def test_update_hash_set_record(self):
        self.redis.update_hash_set_record(self.hset_name, self.hset_id, self.hset_update)
        self.assertDictEqual(self.hset_update, self.redis.get_hash_set_record(self.hset_name, self.hset_id))

    def test_delete_hash_set_record(self):
        self.redis.delete_hash_set_record(self.hset_name, self.hset_id)
        self.assertEqual(None, self.redis.get_hash_set_record(self.hset_name, self.hset_id))


if __name__ == '__main__':
    unittest.main()

class StreamConfig:
    REDIS_SERVER = "localhost"
    REDIS_PORT = 6379
    REDIS_PASSWORD = ""
    # consumer
    CONSUMER_LOGGER = False
    CONSUMER_LOGGER_PATH = ""
    MAX_EVENTS_COUNT = 500
    CONSUMER_BLOCK_TIMEOUT = 60000  # milliseconds
    # producer
    PRODUCER_LOGGER = False
    PRODUCER_LOGGER_PATH = ""
    # algorithm operation
    ALGORITHM_OPERATION_LOGGER = False
    ALGORITHM_OPERATION_LOGGER_PATH = ""
    ID_HASH_STRING_LENGTH = 10

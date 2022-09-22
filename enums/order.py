import numpy as np


class Order:
    INDEX = "index"
    TIME = 'time'
    MARKET = 'market'
    ORDER_ID = 'orderId'
    PRICE = 'price'
    VOLUME = 'volume'
    STATUS = 'status'
    TYPE = 'type'
    SIDE = 'side'
    COM_FEE = 'commission'
    EXECUTED_QTY = 'filled'
    ORDERBOOKID = 'orderbookid'
    TRADES = "trades"
    ERROR = "error"

    class OrderStatus:
        ACTIVE = "Active"
        PARTIAL = "Partial_Filled"
        PARTIAL_CANCELED = "Partial_Canceled"
        FILLED = "Filled"
        CANCELED = "Canceled"
        UNKNOWN = "Unknown"
        ERROR = "error"

    class OrderSide:
        BUY = "BUY"
        SELL = "SELL"

    class OrderError:
        INSUFFICIENT_BALANCE_ERROR = "insufficient_balance_error"
        TIMEOUT_ERROR = "timeout_error"
        INVALID_API_TOKEN_ERROR = "invalid_api_token_error"
        OTHER_ERROR = "other_error"


ORDERS_DTYPE = np.dtype([
    (Order.INDEX, np.int32),
    (Order.ORDER_ID, "U100"),
    (Order.MARKET, "U10"),
    (Order.SIDE, "U5"),
    (Order.PRICE, np.float64),
    (Order.VOLUME, np.float64),
    (Order.EXECUTED_QTY, np.float64),
    (Order.STATUS, "U10"),
    (Order.TYPE, "U10"),
    (Order.COM_FEE, np.float64),
    (Order.TIME, np.float64),
    (Order.ERROR, "U10"),
])

# mapping from enums to shm matrix index for each row
ORDERS_INDEX_MAPPING = dict()
for i in range(len(ORDERS_DTYPE.fields.keys())):
    ORDERS_INDEX_MAPPING[list(ORDERS_DTYPE.fields.keys())[i]] = i

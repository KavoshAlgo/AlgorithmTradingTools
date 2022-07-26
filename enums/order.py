class Order:
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
    Trades = 'trades'
    EVENT_TYPE = 'event_type'

    class OrderStatus:
        ACTIVE = "Active"
        PARTIAL = "Partial_Filled"
        PARTIAL_CANCELED = "Partial_Canceled"
        FILLED = "Filled"
        CANCELED = "Canceled"

    class OrderSide:
        BUY = "BUY"
        SELL = "SELL"

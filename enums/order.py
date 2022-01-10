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

    class OrderStatus:
        ACTIVE = "Active"
        PARTIAL = "Partial_Filled"
        FILLED = "Filled"
        CANCELED = "Canceled"

    class OrderSide:
        BUY = "BUY"
        SELL = "SELL"

class Orderbooks:
    MARKET = 'market'
    ID = 'id'
    ISIN = 'isin'
    LAST_TRADING_DATE = 'last_trading_date'
    SIZE = 'size'
    TIME = 'time'
    CLOSE = 'close'
    LOW = 'low'
    HIGH = 'high'
    INITIAL_MARGIN = 'initial_margin'
    LAST_PRICE = 'last_price'
    YESTERDAY_PRICE = 'yesterday_price'
    BIDS = 'bids'
    ASKS = 'asks'
    EVENT_TYPE = 'event_type'


class OrderbookMatrix:
    INDEX = "index"

    ASK_PRICE = "ask_price"
    ASK_VOLUME = "ask_volume"
    ASK_NET = "ask_net"
    ASK_USD_VALUE = "ask_usd_value"

    BID_PRICE = "bid_price"
    BID_VOLUME = "bid_volume"
    BID_NET = "bid_net"
    BID_USD_VALUE = "bid_usd_value"

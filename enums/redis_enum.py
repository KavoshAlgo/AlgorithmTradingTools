class RedisEnums:
    class Hashset:
        ORDERS = "_orders_"
        OPEN_ORDERS = "_open_orders_"
        TRADES = "_trades_"
        PORTFOLIO = "_portfolio_"

    class Set:
        ORDERBOOK = "_orderbook_"
        EXCHANGE_INFO = "_exchange_info"

    class Sortedset:
        Send_Edit_Error = "_send&edit&error_"
        Trade = "_trade_"

    class Stream:
        MARKET = "_market_data"  # standard: BROKER_NAME + Stream.MARKET
        USER_DATA = "_broker_user_data_"  # standard: BROKER_NAME + Stream.USER_DATA + USERNAME
        USER_REQUEST = "_broker_user_request_"  # standard: BROKER_NAME + Stream.USER_REQUEST + USERNAME

    class Signal:
        TRAP_CANCEL_SIGNAL = "_trap_cancel_signal_"  # standard: BROKER_NAME + Signals.TRAP_CANCEL_SIGNAL + USERNAME

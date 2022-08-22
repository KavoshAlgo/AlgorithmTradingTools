class ExchangeInfo:
    MODE = 'mode'  # MODE OF INCLUDING DECIMAL
    TICK_SIZE = 'tick_size'  # PRICE DECIMAL
    LOT = 'lot'  # VOLUME DECIMAL

    COINS = 'coins'  # COINS OF EXCHANGE
    MARKETS = "markets"  # MARKETS OF EXCHANGE

    MIN_VOL = 'min_vol'  # MIN TRADE VOLUME
    MIN_VALUE = 'min_value'  # MIN TRADE VALUE
    COMMISSION = 'commission'  # COMMISSION FEE OF MARKET

    ORDERBOOK_MAPPING = "orderbook_mapping"  # mapping for orderbook matrix indices
    PORTFOLIO_MAPPING = "portfolio_mapping"  # mapping for portfolio matrix indices
    ORDERBOOK_MATRIX_SHAPE = "orderbook_matrix_shape"  # shape of orderbook matrix
    PORTFOLIO_MATRIX_SHAPE = "portfolio_matrix_shape"  # shape of portfolio matrix

    """ SPECIFIC ENUMS FOR TSETMC STOCK MARKET """
    MARKET_FA = 'market_fa'
    TSETMC_LINK_ID = 'tsetmc_link_id'
    ISIN = 'isin'
    MAX_PRICE_RANGE = 'max_price_range'
    MIN_PRICE_RANGE = 'min_price_range'

    class TruncateMode:
        STEP = 'step'  # E.G. 0.0001 OR 10
        ROUND = 'round'  # E.G 5 , 6 ...

    class CommissionMode:
        MAKER = 'maker'  # COMMISSION FEE OF MAKER TRADES
        TAKER = 'taker'  # COMMISSION FEE OF TAKER TRADES

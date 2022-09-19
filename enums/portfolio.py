import numpy as np


class Portfolio:
    TIME = 'time'
    AVAILABLE_VOL = 'available_vol'
    BLOCKED_VOL = 'blocked_vol'
    TOTAL_VOL = 'total_vol'
    SYMBOL = 'symbol'
    EVENT_TYPE = 'event_type'
    IRT_VALUE = "irt_value"
    USD_VALUE = "usd_value"


class FuturePortfolio(Portfolio):
    SYMBOL = 'symbol'
    SELL_VOL = 'sell_vol'
    BUY_VOL = 'buy_vol'
    CONTRACT_ID = 'contract_id'


class PortfolioMatrix:
    INDEX = "index"
    VOLUME = "volume"
    USD_VALUE = "usd_value"


PORTFOLIO_DTYPE = np.dtype([
    (PortfolioMatrix.INDEX, np.int32),
    (PortfolioMatrix.VOLUME, np.float64),
    (PortfolioMatrix.USD_VALUE, np.float64),
])
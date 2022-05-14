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

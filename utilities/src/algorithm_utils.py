def validate_orderbooks(orderbooks: list):
    for orderbook in orderbooks:
        if orderbook is None or 'bids' not in orderbook or 'asks' not in orderbook:
            return False
        if len(orderbook['bids']) <= 0 or len(orderbook['asks']) <= 0:
            return False
        if orderbook['bids'][0][0] >= orderbook['asks'][0][0]:
            return False
    return True

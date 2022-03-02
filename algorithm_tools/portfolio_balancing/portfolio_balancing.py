import threading
import time

from monitoring.src.logger import Logger

from storage.redis.src.redis import Redis

from enums.redis_enum import RedisEnums
from enums.orderbooks import Orderbooks
from enums.portfolio import Portfolio
from enums.order import Order

from events.event import Event


# TODO fix naming and basic (flow chart)
# TODO edit def main to new version
# TODO Write def check_coudition
# TODO Write def ex_change_usdtirt
# TODO Write def get_usdt_irt_portfolio

class PortfolioBalancing:

    def __init__(self, username, broker, trade_value_threshold=0, portfolio_balance_threshold=0,
                 threshold_factor=0, vol_factor=0, extra_price=0, execution_wait_time=120):
        self.redis = Redis()
        self.logger = Logger(True, '')
        self.trade_value_threshold = trade_value_threshold
        self.portfolio_balance_threshold = portfolio_balance_threshold
        self.threshold_factor = threshold_factor
        self.vol_factor = vol_factor
        self.extra_price = extra_price
        self.execution_wait_time = execution_wait_time
        self.broker = broker
        self.username = username
        self.market = 'USDTIRT'
        self.USDT = 'USDT'
        self.IRT = 'IRT'

    def start(self):
        try:
            threading.Thread(name="main", target=self.main, daemon=False).start()
        except Exception as ex:
            self.logger.error("Could not start the manage requests :" + str(ex))

    def main(self, broker):
        pass

    def check_coudition(self, condition, usdt_portfolio, irt_portfolio):
        pass

    def send_order(self):
        pass

    def ex_change_usdtirt(self):
        pass

    def get_usdt_irt_portfolio(self, broker, username):
        pass


if __name__ == '__main__':
    pass

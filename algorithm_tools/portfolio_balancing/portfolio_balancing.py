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
# TODO Write def ex_change_usdtirt

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
        while True:
            usdt_portfolio, irt_portfolio = self.get_usdt_irt_portfolio(broker, self.username)
            if self.check_condition("condition1", usdt_portfolio, irt_portfolio):
                time.sleep(self.execution_wait_time)
                usdt_portfolio, irt_portfolio = self.get_usdt_irt_portfolio(broker, self.username)
                if self.check_condition("condition1", usdt_portfolio, irt_portfolio):
                    self.send_order()
            if self.check_condition("condition2", usdt_portfolio, irt_portfolio):
                time.sleep(self.execution_wait_time)
                usdt_portfolio, irt_portfolio = self.get_usdt_irt_portfolio(broker, self.username)
            if self.check_condition("condition2", usdt_portfolio, irt_portfolio):
                self.send_order()

    def check_condition(self, condition, usdt_portfolio, irt_portfolio):
        if condition == "condition1":
            first_con = usdt_portfolio < self.trade_value_threshold
            second_con = irt_portfolio > self.threshold_factor * self.trade_value_threshold
            third_con = self.trade_value_threshold < usdt_portfolio < self.portfolio_balance_threshold
            fourth_con = irt_portfolio > self.threshold_factor * self.portfolio_balance_threshold
            if (first_con and second_con) or (third_con and fourth_con):
                return True
            else:
                return False
        elif condition == "condition2":
            con_five = self.trade_value_threshold < usdt_portfolio < self.portfolio_balance_threshold
            con_six = irt_portfolio > self.threshold_factor * self.portfolio_balance_threshold
            con_seven = self.trade_value_threshold < irt_portfolio < self.portfolio_balance_threshold
            con_eight = usdt_portfolio > self.threshold_factor * self.portfolio_balance_threshold
            if (con_five and con_six) or (con_seven and con_eight):
                return True

    def send_order(self):
        pass

    def ex_change_usdtirt(self):
        pass

    def get_usdt_irt_portfolio(self, broker, username):
        try:
            usdt_portfolio = self.redis.get_hash_set_record(broker + RedisEnums.Hashset.PORTFOLIO + username,
                                                            self.USDT[Portfolio.AVAILABLE_VOL])
            irt_portfolio = self.redis.get_hash_set_record(broker + RedisEnums.Hashset.PORTFOLIO + username,
                                                           self.IRT[Portfolio.AVAILABLE_VOL])
            if usdt_portfolio is not None and irt_portfolio is not None:
                return usdt_portfolio, irt_portfolio
            else:
                raise Exception('there is a problem in get portfolio %s - %s' % (usdt_portfolio, irt_portfolio))
        except Exception as ex:
            self.logger.error(ex)


if __name__ == '__main__':
    pass

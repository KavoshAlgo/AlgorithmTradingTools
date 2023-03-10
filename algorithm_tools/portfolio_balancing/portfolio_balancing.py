import threading
import time
import asyncio

from monitoring.src.logger import Logger

from storage.redis.src.redis import Redis

from enums.redis_enum import RedisEnums
from enums.orderbooks import Orderbooks
from enums.portfolio import Portfolio
from enums.order import Order


class PortfolioBalancing:
    def __init__(self, username, broker_object, broker_name, trade_value_threshold=20, portfolio_balance_threshold=200,
                 threshold_factor=2, vol_factor=0.5, extra_price=100, execution_wait_time=120, is_event_base=False):
        """ initial class essential objects and agents """
        self.redis = Redis()
        self.logger = Logger(False, '')
        self.broker = broker_object
        """ PortfolioBalancing configs """
        self.broker_name = broker_name
        self.username = username
        self.trade_value_threshold = trade_value_threshold
        self.portfolio_balance_threshold = portfolio_balance_threshold
        self.threshold_factor = threshold_factor
        self.vol_factor = vol_factor
        self.extra_price = extra_price
        self.execution_wait_time = execution_wait_time
        """ PortfolioBalancing ENUMS """
        self.market = 'USDTIRT'
        self.USDT = 'USDT'
        self.IRT = 'IRT'
        """ Event base """
        self.is_event_base = is_event_base
        self.loop = None

    def start(self):
        """ create one thread on main method """
        try:
            threading.Thread(name="main", target=self.main, daemon=False).start()
        except Exception as ex:
            self.logger.error("Could not start the main method :" + str(ex))

    def main(self):
        """ check portfolio If needed to send order """
        while True:
            usdt_portfolio, irt_portfolio = self.get_usdt_irt_portfolio()
            if self.check_condition("condition1", usdt_portfolio, self.change_usdtirt(irt_portfolio)):
                time.sleep(self.execution_wait_time)
                usdt_portfolio, irt_portfolio = self.get_usdt_irt_portfolio()
                if self.check_condition("condition1", usdt_portfolio, self.change_usdtirt(irt_portfolio)):
                    self.send_order(
                        side=Order.OrderSide.BUY,
                        price=float(self.get_usdt_irt_orderbook()[Orderbooks.ASKS][0][0]) + self.extra_price,
                        vol=self.vol_factor * self.change_usdtirt(irt_portfolio)
                    )
            if self.check_condition("condition2", usdt_portfolio, self.change_usdtirt(irt_portfolio)):
                time.sleep(self.execution_wait_time)
                usdt_portfolio, irt_portfolio = self.get_usdt_irt_portfolio()
                if self.check_condition("condition2", usdt_portfolio, self.change_usdtirt(irt_portfolio)):
                    self.send_order(
                        side=Order.OrderSide.SELL,
                        price=float(self.get_usdt_irt_orderbook()[Orderbooks.BIDS][0][0]) - self.extra_price,
                        vol=self.vol_factor * usdt_portfolio
                    )

    def check_condition(self, condition, usdt_portfolio, irt_portfolio):
        """ check portfolio to always in balance """
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
            con_five = irt_portfolio < self.trade_value_threshold
            con_six = usdt_portfolio > self.threshold_factor * self.trade_value_threshold
            con_seven = self.trade_value_threshold < irt_portfolio < self.portfolio_balance_threshold
            con_eight = usdt_portfolio > self.threshold_factor * self.portfolio_balance_threshold
            if (con_five and con_six) or (con_seven and con_eight):
                return True
            else:
                return False

    def send_order(self, side, price, vol):
        """ send order method """
        if not self.is_event_base:
            order, status = self.broker.send_order(
                market=self.market,
                side=side,
                price=price,
                volume=vol
            )
            if status == 'ok':
                self.logger.warning('balance USDT-IRT with order : %s' % order)
            else:
                self.logger.error('balance USDT-IRT can`t send order : %s ' % order)
        elif self.is_event_base:
            asyncio.run(self.send_order_event(price=price, side=side, vol=vol))

    async def send_order_event(self, side, price, vol):
        """ send_order_event use for Evnet base program """
        self.loop = asyncio.get_event_loop()
        send_order_event = await self.broker.send_order(
            market=self.market,
            side=side,
            price=price,
            volume=vol,
            loop=self.loop
        )
        await send_order_event.wait()
        if send_order_event.EVENT_VALUE['status'] == 'ok':
            self.logger.warning('balance USDT-IRT with order : %s' % send_order_event.EVENT_VALUE['response'])
        else:
            self.logger.error('balance USDT-IRT can`t send order : %s ' % send_order_event.EVENT_VALUE['response'])

    def change_usdtirt(self, irt_portfolio):
        """ change TOMAN to USDT """
        order_book = self.get_usdt_irt_orderbook()
        return irt_portfolio / float(order_book[Orderbooks.ASKS][0][0])

    def get_usdt_irt_portfolio(self):
        """ get portfolio data from redis"""
        try:
            usdt_portfolio = self.redis.get_hash_set_record(self.broker_name +
                                                            RedisEnums.Hashset.PORTFOLIO +
                                                            self.username,
                                                            self.USDT
                                                            )[Portfolio.AVAILABLE_VOL]
            irt_portfolio = self.redis.get_hash_set_record(self.broker_name +
                                                           RedisEnums.Hashset.PORTFOLIO +
                                                           self.username,
                                                           self.IRT
                                                           )[Portfolio.AVAILABLE_VOL]
            if usdt_portfolio is not None and irt_portfolio is not None:
                return usdt_portfolio, irt_portfolio
            else:
                raise Exception('there is a problem in get portfolio %s - %s' % (usdt_portfolio, irt_portfolio))
        except Exception as ex:
            self.logger.error(ex)

    def get_usdt_irt_orderbook(self):
        """ get data from order book on redis"""
        while True:
            response = self.redis.get_set_record(self.broker_name + RedisEnums.Set.ORDERBOOK + self.market)
            if response is not None:
                return response


if __name__ == '__main__':
    pass

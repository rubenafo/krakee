import logging
import logging as logger
from functools import wraps

import krakenex
from pandas import DataFrame
from pykrakenapi import KrakenAPI

from krakee import OrderBuilder
from krakee.api import validators


# @cache decorator to cache responses
def cached(*args, **kwargs):

    func = None
    if len(args) == 1 :
        func = args[0]
    if func:
        always = False
    if not func:
        always = kwargs.get('always')

    def callable (func):

        @wraps (func)
        def wrapper(self, *args, **kwargs):
            func_name = func.__name__
            cachedValue = None
            cachedId = "_".join([func_name, *args])
            if self.is_cached or always:
                if cachedId in self.cache:
                    cachedValue = self.cache[cachedId]
                    logger.info ("Retrieving {}() from cache...".format(func_name))
            if cachedValue is None:
                cachedValue = func(self, *args, **kwargs)
                if self.cache or always:
                    self.cache[cachedId] = cachedValue
            return cachedValue
        return wrapper
    return callable(func) if func else callable


class Krakee:

    def __init__(self, authfile=None, cached=False):
        self.cache = {}
        self.is_cached = cached
        if authfile:
            with open(authfile, 'r') as f:
                public_key = f.readline().strip()
                secret_key = f.readline().strip()
                self.kapi = KrakenAPI(krakenex.API(public_key, secret_key))
                logger.info("Auth keys successfully loaded from {}".format(authfile))
        else:
            self.kapi = KrakenAPI(krakenex.API())
            logger.info("Auth token not provided, only public API available")
        self.assetPairs()

    @cached(always=True)
    def assets(self) -> DataFrame: return self.kapi.get_asset_info().transpose()

    @cached (always=True)
    def assetPairs(self) -> DataFrame: return self.kapi.get_tradable_asset_pairs().transpose()

    @cached
    def tickers(self, *pairs) -> DataFrame:
        [validators.asset_pair(self, pair) for pair in pairs]
        return self.kapi.get_ticker_information(",".join(pairs)).transpose()

    @cached
    def ohlc(self, pair, interval: str = "1min", since=None) -> DataFrame:
        validators.asset_pair (self, pair)
        intervals = {"1min": 1, "5min": 5, "15min": 15, "30min": 30, "1h": 60, "4h": 240, "1d": 1440, "7d": 10080, "15d": 21600}
        validators.assert_interval(interval, intervals)
        return self.kapi.get_ohlc_data(pair, intervals, since)


    @cached
    def orderBook(self, pair, count=None) -> (DataFrame, DataFrame):
        validators.asset_pair(self, pair)
        return self.kapi.get_order_book(pair, count)

    @cached
    def trades(self, pair, since=None) -> DataFrame:
        validators.asset_pair(self, pair)
        return self.kapi.get_recent_trades (pair, since)

    @cached
    def spread(self, pair, since=None) -> DataFrame:
        validators.asset_pair(self, pair)
        return self.kapi.get_recent_spread_data (pair, since)

    # Private API

    def addOrder (self, order_builder: OrderBuilder):
        return self.kapi.api.query_private("AddTrade", order_builder.build())

    def balance(self): return self.kapi.get_account_balance()

    def tradeBalance (self): return self.kapi.get_trade_balance()

    def openOrders (self): return self.kapi.get_open_orders()
    def closedOrders (self): return self.kapi.get_closed_orders()

logging.basicConfig(level=logging.INFO)
k = Krakee("/home/tatil/.kr_r", cached=True)

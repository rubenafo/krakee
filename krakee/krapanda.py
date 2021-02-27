import logging
import logging as logger

import krakenex
from pandas import DataFrame
from pykrakenapi import KrakenAPI

class Krapanda:

    def __init__(self, authfile=None):
        self.cache = {}
        if authfile:
            with open(authfile, 'r') as f:
                public_key = f.readline().strip()
                secret_key = f.readline().strip()
                self.kapi = KrakenAPI(krakenex.API(public_key, secret_key))
                logger.info("Auth keys successfully loaded from ", authfile)
        else:
            self.kapi = KrakenAPI(krakenex.API())
            logger.info("Auth token not provided, only public API available")
        self.cache['assetPairs'] = self.assetPairs()

    def assets(self) -> DataFrame: return self.kapi.get_asset_info().transpose()

    def assetPairs(self) -> DataFrame: return self.kapi.get_tradable_asset_pairs().transpose()

    def ticker(self, *pairs) -> DataFrame:
        for pair in pairs:
            assert (pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        return self.kapi.get_ticker_information(",".join(pairs)).transpose()

    def ohlc(self, pair, interval: str, since=None) -> DataFrame:
        assert (pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        valid_intervals = {"1min": 1, "5min": 5, "15min": 15, "30min": 30, "1h": 60, "4h": 240, "1d": 1440, "7d": 10080, "15d": 21600}
        assert (interval in valid_intervals), "{} interval not in {}".format(interval, list(valid_intervals.keys()))
        return self.kapi.get_ohlc_data(pair, valid_intervals[interval], since)

    def orderBook(self, pair, count=None) -> (DataFrame, DataFrame):
        assert (pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        return self.kapi.get_order_book(pair, count)

    def trades(self, pair, since=None) -> DataFrame:
        assert (pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        return self.kapi.get_recent_trades (pair, since)

    def spread(self, pair, since=None) -> DataFrame:
        assert(pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        return self.kapi.get_recent_spread_data (pair, since)

    # Private API

logging.basicConfig(level=logging.INFO)
k = Krapanda("/home/tatil/.kr_r")

k.cache

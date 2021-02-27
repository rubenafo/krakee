from pandas import DataFrame


class PublicApi:

    def __init__(self, kapi, cache: dict):
        self.kapi = kapi
        self.cache = cache

    def assets(self) -> DataFrame:
        df = self.kapi.query_public("Assets")
        return DataFrame(df['result'])

    def assetPairs(self) -> DataFrame:
        df = self.kapi.query_public("AssetPairs")
        return DataFrame(df['result'])

    def ticker(self, *pairs) -> DataFrame:
        df = self.kapi.query_public("Ticker", data="pair=" + ",".join(pairs))
        return DataFrame(df['result'])

    def ohlc(self, pair, interval: str, since=None) -> DataFrame:
        assert (pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        valid_intervals = {"1min":1, "5min":5, "15min":15, "30min": 30, "1h":60, "4h":240, "1d":1440, "7d":10080, "15d":21600}
        assert (interval in valid_intervals)
        data = "pair={}&interval={}".format(pair, valid_intervals[interval])
        if since:
            data = "{}&since={}".format(data, since)
        response = self.kapi.query_public("OHLC", data=data)
        rows = response['result'][pair]
        ohlcdata = DataFrame.from_records(rows, columns=['time', 'o', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        last = response['result']['last']
        return ohlcdata, last

    def orderBook(self, pair, count=None) -> DataFrame:
        assert (pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        data = "pair={}".format(pair)
        if count:
            data = "{}&count={}".format(data, count)
        response = self.kapi.query_public("Depth", data)
        asks = response['result'][pair]['asks']
        bids = response['result'][pair]['bids']
        asksDf = DataFrame.from_records(asks, columns=['price', 'volume', 'timestamp'])
        bidsDf = DataFrame.from_records(bids, columns=['price', 'volume', 'timestamp'])
        asksDf['type'] = 'asks'
        bidsDf['type'] = 'bids'
        return asksDf.append(bidsDf, ignore_index=True)

    def trades(self, pair, since=None) -> DataFrame:
        assert (pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        data = "pair={}".format(pair)
        if since:
            data = "{}&since={}".format(data, since)
        response = self.kapi.query_public("Trades", data)
        last = response['result']['last']
        return DataFrame.from_records(
            response['result'][pair], columns=['price', 'volume', 'time', 'direction', 'type', 'misc']), last

    def spread(self, pair, since=None) -> DataFrame:
        assert(pair in list(self.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)
        data = "pair={}".format(pair)
        if since:
            data = "{}&since={}".format(data, since)
        response = self.kapi.query_public("Spread", data)
        last = response['result']['last']
        return DataFrame.from_records(response['result'][pair], columns=['time', 'bid', 'ask']), last

    # Private API

    def balance(self) -> DataFrame:
        response = self.kapi.query_private("Balance")
        return DataFrame(response['result'], index=[0], dtype=float)

    def openOrders(self):
        response = self.kapi.query_private("OpenOrders")

    def closedOrders(self, start, end) -> DataFrame:
        data = {'start': start, 'end': end}
        response = self.kapi.query_private("ClosedOrders", data)
        closedOrders = response['result']['closed']
        df = DataFrame.from_dict(closedOrders, orient='index')
        df['txId'] = df.index
        return df

    def tradesHistory(self, start=None, end=None) -> DataFrame:
        data = {}
        if start:
            data['start'] = start
        if end:
            data['end'] = end
        response = self.kapi.query_private("TradesHistory", data)
        df = DataFrame.from_dict(response['result']['trades'], orient='index')
        df['txId'] = df.index
        return df

    def addorder (self, order: dict) :
        assert (order), "order cannot be empty"
        try:
            return self.kapi.query_private("AddOrder", order)
        except (HTTPError):
            return None

    def calculateBalance (self):
        userHoldings = self.balance()
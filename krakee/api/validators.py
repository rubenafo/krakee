
def asset_pair (pair, krakee):
    assert (pair in list(krakee.cache['assetPairs'].columns)), "Invalid pair: {}".format(pair)

def assert_interval (interval, intervals):
    assert (interval in intervals), "{} interval not in {}".format(interval, list(intervals.keys()))
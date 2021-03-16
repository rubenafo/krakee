from numpy import number
from pandas import DataFrame, Series

VALID_TYPES = ["open", "high", "low", "close", "volume", "vwap", "count"]


class OhlcDataFrame(DataFrame):

    def __init__(self, src_values: DataFrame):
        DataFrame.__init__(self, src_values.values, columns=src_values.columns, index=src_values.index)

    def get_by_asset_pair_and_type(self, asset_pair: str, type: str):
        assert type in VALID_TYPES, "Invalid type: {}, valid types={}".format(type, VALID_TYPES)
        return self["{}_{}".format(type, asset_pair)]
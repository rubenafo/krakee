from pandas import DataFrame, Series


class OhlcDataFrame(DataFrame):

    def __init__(self, src_values: DataFrame):
        DataFrame.__init__(self, src_values.values, columns=src_values.columns, index=src_values.index)

    def get_open (self, asset_pair: str) -> Series:
        return self["open_{}".format(asset_pair)]

    def get_close(self, asset_pair: str) -> Series:
        return self["close_{}".format(asset_pair)]

    def get_high(self, asset_pair: str) -> Series:
        return self["high_{}".format(asset_pair)]

    def get_low(self, asset_pair: str) -> Series:
        return self["low_{}".format(asset_pair)]

    def get_volume(self, asset_pair: str) -> Series:
        return self["volume_{}".format(asset_pair)]

    def get_vwap(self, asset_pair: str) -> Series:
        return self["vwap_{}".format(asset_pair)]

    def get_count(self, asset_pair: str) -> Series:
        return self["count_{}".format(asset_pair)]
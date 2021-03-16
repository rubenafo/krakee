from __future__ import annotations

from pandas import DataFrame


class AssetDataFrame(DataFrame):

    def __init__(self, src_values: DataFrame):
        DataFrame.__init__(self, src_values.values, columns=src_values.columns, index=src_values.index)

    def by_asset_name(self, asset_name:str) -> AssetDataFrame:
        asset_name = asset_name.upper()
        assert asset_name in list(self.columns), \
            "Unknown asset name: {} - valid values: {}".format(asset_name, list(self.columns))
        return self[asset_name]

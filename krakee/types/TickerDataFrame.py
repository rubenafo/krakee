from __future__ import annotations

from pandas import DataFrame, Series


class TickerDataFrame (DataFrame):

    def __init__(self, src_values: DataFrame):
        mappings = {'ask_today': ('a',0), 'ask_whole_lot_volume': ('a',1), 'ask_lot_volume':('a',2),
                    'bid_today': ('b',0), 'bid_whole_lot_volume': ('b',1), 'bid_lot_volume':('b',2),
                    'volume_today': ('v', 0), 'volume_24h':('v', 1),
                    'volume_weighted_today': ('p', 0), 'volume_weighted_24h':('p', 1),
                    'trades_today':('t', 0), 'trades_24h': ('t', 1),
                    'low_today':('l', 0), 'low_24h':('l', 1),
                    'high_today':('h', 0), 'high_24h':('h', 1),
                    'last_trade_close_price':('c', 0), 'last_trade_close_volume':('c', 1)
                    }
        for new_col in mappings.keys():
            src_values.loc[new_col] = list(map(lambda x: x[mappings[new_col][1]], src_values.loc[mappings[new_col][0]]))
        src_values.loc['open'] = list(map(lambda x: x, src_values.loc['o']))
        src_values = src_values.drop(labels=['c', 'a', 'b', 'v', 'p', 't', 'l', 'h', 'o'])
        DataFrame.__init__(self, src_values.values, columns=src_values.columns, index=src_values.index)

    def asset_pairs_sorted_by (self, row_name: str) -> Series:
        return self.loc[row_name].sort_values(ascending=False)
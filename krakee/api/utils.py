from typing import Dict

import pandas
import pandas as pd

def assert_list (elem, param_name):
    assert (type(elem) == list), "{} parameter should be a list, type={} found".format(param_name, type(elem))

def asset_pair (krakee, pair):
    if type(pair) == list:
        for pair in pair:
            assert (pair in list(krakee.asset_pairs().columns)), "Invalid pair: {}".format(pair)
    else:
        assert (pair in list(krakee.asset_pairs().columns)), "Invalid pair: {}".format(pair)

def assert_interval (interval, intervals):
    assert (interval in intervals), "{} interval not in {}".format(interval, list(intervals.keys()))

def dataframe_to_numeric(df):
    for i in list(df.columns):
        for j in list(df.index):
            df[i][j] = pd.to_numeric(df[i][j])
    return df


def merge_ohlc (data: Dict[str, tuple]) -> pd.DataFrame:
    first_asset_pair = list(data.keys())[0]
    first_df = data[first_asset_pair][0]
    df_columns = {colname: colname + "_" + first_asset_pair for colname in list(first_df.columns)}
    first_df = first_df.rename(columns=df_columns)
    for asset_pair in list(data.keys())[1:]:
        first_df = first_df.join(data[asset_pair][0], rsuffix="_" + asset_pair)
    return first_df
from datetime import timedelta, datetime
from typing import Dict, List

import pandas as pd
from pandas import DataFrame


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


def merge_ohlc (data: Dict[str, tuple]) -> DataFrame:
    renamed_dfs = []
    for asset_pair in list(data.keys()):
        df = data[asset_pair][0]
        new_columns = {colname: colname + "_" + asset_pair for colname in list(df.columns)}
        renamed_dfs.append(df.rename(columns=new_columns))
    for df in renamed_dfs[1:]:
        renamed_dfs[0] = renamed_dfs[0].join(df)
    return renamed_dfs[0]


def as_list (values) -> List:
    if type(values) == list:
        return values
    if type(values) == tuple:
        if type(values[0]) == list:
            return values[0]
        else:
            return list(values)
    return [values]


"""
Returns epoch timestamp from previous date
Parameters:
days: number of past days to obtain epoch from
hours: number of past hours to obtain epoch from
start_time: optional datetime to be considered as now(). now() if undefined 
"""
def epoch_delta (days=None, hours=None, start_time=datetime.now()):
    delta_time = None
    if days and hours:
        delta_time = timedelta(days=days, hours=hours)
    else:
        if days:
            delta_time = timedelta(days=days)
        elif hours:
            delta_time = timedelta(hours=hours)
    delta_date = start_time - delta_time
    return int(delta_date.timestamp())

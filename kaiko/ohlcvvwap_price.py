"""
For Asset metrics, I only will take the total trading amount, and how each exchange is performing on this asset
for this period of time.
"""
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import datetime
import requests
import os

from kaiko.resources import KAIKO_API_KEY
from tool_funcs.resources import write_api


# noinspection PyShadowingNames
def get_ohlcvvwap_data(start_time, end_time, exchange, pair, interval, bucket_name, measurement_name):
    url = ('https://us.market-api.kaiko.io/v2/data/trades.v1/exchanges'
           f'/{exchange}/spot'
           f'/{pair}/aggregations/count_ohlcv_vwap'
           f'?start_time={start_time}'
           f'&end_time={end_time}'
           '&sort=desc'
           f'&interval={interval}'
           f'&page_size=100000')
    print(url)
    headers = {
        'X-Api-Key': KAIKO_API_KEY,
    }

    response = requests.get(url, headers=headers)

    data = response.json()['data']
    df = pd.DataFrame(data)

    while 'next_url' in response.json():
        next_url = response.json()['next_url']
        response = requests.get(next_url, headers=headers)
        data = response.json()['data']
        df = pd.concat([df, pd.DataFrame(data)])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['price'] = df['price'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df = df.dropna()
    print(df)

    # Handle and Upload overall metrics: iterate through each row
    points = []
    for i, row in df.iterrows():
        p = influxdb_client.Point(measurement_name) \
            .tag("pair", pair) \
            .field("price", row['price']) \
            .field("volume", row['volume']) \
            .time(row['timestamp'], WritePrecision.NS)

        points.append(p)

    write_api.write(bucket_name, record=points)
    print(f"Uploaded {len(df)} data to influxdb!")


if __name__ == '__main__':
    # start time is 10 seconds ago
    params = {
        "start_time": (datetime.datetime.utcnow() - datetime.timedelta(seconds=10000)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "end_time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "exchange": "bbsp",
        "pair": "sol-usdc",
        "interval": "1s",
        "bucket_name": "test_bucket",
        "measurement_name": "ohlcvvwap_test4"
    }

    get_ohlcvvwap_data(**params)

    params = {
        "start_time": (datetime.datetime.utcnow() - datetime.timedelta(seconds=10000)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "end_time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "exchange": "binc",
        "pair": "sol-usdt",
        "interval": "1s",
        "bucket_name": "test_bucket",
        "measurement_name": "ohlcvvwap_test4"
    }

    get_ohlcvvwap_data(**params)
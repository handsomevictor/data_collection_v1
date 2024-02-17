import os
import csv
import json
import time
import datetime
import requests
import threading

from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision

# from tool_funcs.upload_to_influxdb import upload_to_influxdb
from tool_funcs.resources import write_api

TMP_DATABASE_DIR = os.path.join(os.path.dirname(__file__), "..", "tmp", "database")

if not os.path.exists(TMP_DATABASE_DIR):
    os.makedirs(TMP_DATABASE_DIR)


def get_unit_buy_price(base, quote):
    url = f'https://price.jup.ag/v4/price?ids={base}&vsToken={quote}'
    response = requests.get(url)
    data = response.json()
    return (data['data'][base]['id'],
            data['data'][base]['vsToken'],
            data['data'][base]['price'],
            data['timeTaken'])


def save_unit_buy_price(base, quote, measurement_name="unit_buy_price", bucket_name="test_bucket"):
    base_id, quote_id, price, time_delay = get_unit_buy_price(base, quote)
    time_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    data = {
        "time": time_str,
        "base_id": base_id,
        "quote_id": quote_id,
        "price": price,
        "time_delay": time_delay
    }

    # save to local
    file_path = os.path.join(TMP_DATABASE_DIR, f"{base}_{quote}_price.csv")
    with open(file_path, "a") as f:
        writer = csv.writer(f)
        writer.writerow(data.values())
        print(f"Saved {base} to {quote} price to {file_path}")

    # upload to InfluxDB
    p = Point(measurement_name) \
        .tag("pair", f"{base}_{quote}") \
        .field("price", float(price)) \
        .field("time_delay", float(time_delay)) \
        .time(time_str, WritePrecision.NS)

    write_api.write(bucket=bucket_name, record=p)
    print(f"Uploaded {base} to {quote} price to InfluxDB")

    # except Exception as e:
    #     print(f"Error occurred: {str(e)}")

    # Schedule the next execution
    threading.Timer(1.0 - time.time() % 1.0, save_unit_buy_price,
                    args=(base, quote, measurement_name, bucket_name)).start()


if __name__ == '__main__':
    base = "SOL"
    quote = "USDC"
    measurement_name = "unit_buy_price3"
    bucket_name = "test_bucket"
    save_unit_buy_price(base, quote, measurement_name, bucket_name)

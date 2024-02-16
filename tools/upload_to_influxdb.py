"""
If anyone wants to use this, please add the following to the environment variables:

INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG')
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN')
INFLUXDB_URL = os.environ.get('INFLUXDB_URL')
"""
import datetime

import influxdb_client
from concurrent.futures import ProcessPoolExecutor
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision

from tools.resources import write_api


def upload_to_influxdb(points: list, bucket: str):
    write_api.write(bucket=bucket, record=points)
    print(f"Uploaded to InfluxDB at {datetime.datetime.now(datetime.timezone.utc)}")


if __name__ == '__main__':
    ...

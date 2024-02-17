import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_ORG = os.environ.get('VICTOR_INFLUXDB_ORG')
INFLUXDB_TOKEN = os.environ.get('VICTOR_INFLUXDB_TOKEN')
INFLUXDB_URL = os.environ.get('VICTOR_INFLUXDB_URL')

client = influxdb_client.InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)


if __name__ == '__main__':
    print(f'InfluxDB client created with url: {INFLUXDB_URL} and token: {INFLUXDB_TOKEN} for org: {INFLUXDB_ORG}')

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from config import INFLUXDB_URL
from config import INFLUXDB_TOKEN
from config import INFLUXDB_ORG
from config import INFLUXDB_BUCKET

class InfluxDbWriter:
    def __init__(self,measurement):
        self.bucket_name = INFLUXDB_BUCKET
        self.measurement = measurement
        self.client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_crane_datas(self, data_frame):
        data_dict = data_frame.__dict__
        data_dict_list = list(data_dict.keys())

        self.write_api.write(bucket=self.bucket_name,
                    record=data_dict,
                    record_measurement_name=self.measurement,
                    #record_tag_keys=["engine", "type"],
                    record_field_keys=data_dict_list)


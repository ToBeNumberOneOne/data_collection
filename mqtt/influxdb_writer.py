import asyncio
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

from config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

logger = logging.getLogger(__name__)

class InfluxDbWriter:
    def __init__(self):
        logger.info("Initializing InfluxDbWriter")
        self.bucket_name = INFLUXDB_BUCKET
        self.client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_crane_datas(self, data_frame, measurement):
        logger.debug("Writing crane datas to InfluxDb")
        data_dict = data_frame.__dict__
        data_dict_list = list(data_dict.keys())

        try:
            self.write_api.write(
                bucket=self.bucket_name,
                record=data_dict,
                record_measurement_name=measurement,
                # record_tag_keys=["engine", "type"],
                record_field_keys=data_dict_list
                )
        except Exception as e:
            logger.error(f"Error writing crane datas to InfluxDb: {e}")
        

    async def write_crane_datas_async(self, data_frame, measurement):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.write_crane_datas, data_frame, measurement)

import asyncio
from influxdb_client import InfluxDBClient,Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import logging

from config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET

logger = logging.getLogger(__name__)

class InfluxDbWriter:
    def __init__(self):
        logger.info("Initializing InfluxDbWriter")
        self.bucket_name = INFLUXDB_BUCKET
        self.client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

        #数据缓存后再插入
        self.data_cache = []
        self.batch_size = 100 

    def write_crane_datas(self, data_frame, measurement):
        
        data_dict = data_frame.__dict__

        data_point = Point(measurement).time(datetime.utcnow())

        for key, value in data_dict.items():
            data_point.field(key, value)

        self.data_cache.append(data_point)
        
        if len(self.data_cache) >= self.batch_size:
            try:
                self.write_api.write(bucket=self.bucket_name, record=self.data_cache)
                self.data_cache = []
                logger.info(f"Write {self.batch_size} crane datas to tables")
            except Exception as e:
                logger.error(f"Error writing crane datas to InfluxDb: {e}")
        

    async def write_crane_datas_async(self, data_frame, measurement):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.write_crane_datas, data_frame, measurement)

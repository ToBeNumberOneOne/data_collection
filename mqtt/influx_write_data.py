from dataclasses import dataclass
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

@dataclass
class QcData:
    """
    DataClass structure - Car
    """
    trolleyPos: float
    hoistPos: float
    trolleySpeed: float
    hoistSpeed: float

# influxdb config
url = "http://10.0.0.74:8086" 
token = "hpclmJd-xrebBuf-RzNL1Xhx7wqSQmAWSoEoQ1gpfQRj_mBfuMKNnUUbdPvFVX_gvVk7v8E5idM6xCCvUF41fw=="
org = "jskj"

# 数据插入到influxdb中
def write_qc_data(qc_data,write_api):
    write_api.write(bucket="Test",
                    record=qc_data,
                    record_measurement_name="Qc_his",
                    #record_tag_keys=["engine", "type"],
                    record_field_keys=["trolleyPos","hoistPos","trolleySpeed","hoistSpeed"])


from dataclasses import dataclass
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# influxdb config
url = "http://10.0.0.74:8086" 
token = "hpclmJd-xrebBuf-RzNL1Xhx7wqSQmAWSoEoQ1gpfQRj_mBfuMKNnUUbdPvFVX_gvVk7v8E5idM6xCCvUF41fw=="
org = "jskj"

# 数据插入到influxdb中
def write_crane_data(data_frame,write_api):
    
    data_dict = data_frame.__dict__
    data_dict_list = list(data_dict.keys())
  
    write_api.write(bucket="Test",
                    record=data_dict,
                    record_measurement_name="Crane_his",
                    #record_tag_keys=["engine", "type"],
                    record_field_keys=data_dict_list)


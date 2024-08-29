import asyncio
import paho.mqtt.client as mqtt

from CraneData import CraneDataHandler

# Import configuration
from config import MQTT_BROKER_IP
from config import MQTT_BROKER_PORT
from config import MQTT_TOPICS


from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from influx_write_data import write_crane_data
# influxdb config
url = "http://10.0.0.74:8086" 
token = "hpclmJd-xrebBuf-RzNL1Xhx7wqSQmAWSoEoQ1gpfQRj_mBfuMKNnUUbdPvFVX_gvVk7v8E5idM6xCCvUF41fw=="
org = "jskj"

influxdb_client = InfluxDBClient(url=url, token=token, org=org)
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

data_frame = CraneDataHandler()

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in MQTT_TOPICS:
        client.subscribe(topic)

# Callback when a message is received
def on_message(client, userdata, msg):
    # 解析数据
    data_frame.parse_data(msg.payload)
    write_crane_data(data_frame, write_api)
    #print(msg.topic + data_frame.data_to_json())

async def main():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_IP, MQTT_BROKER_PORT, 60)

    client.loop_start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

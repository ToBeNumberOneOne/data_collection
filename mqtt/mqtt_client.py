import asyncio
import paho.mqtt.client as mqtt

from dataframe_handler import CraneDataHandler
from influxdb_writer import CraneDataWriter

# Import configuration
from config import MQTT_BROKER_IP
from config import MQTT_BROKER_PORT
from config import MQTT_TOPICS

data_frame = CraneDataHandler()
data_writer = CraneDataWriter(measurement='Crane_his')

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in MQTT_TOPICS:
        client.subscribe(topic)

# Callback when a message is received
def on_message(client, userdata, msg):
    # 解析数据
    data_frame.parse_data(msg.payload)
    data_writer.write_crane_datas(data_frame)
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

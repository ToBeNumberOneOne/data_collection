import asyncio

from mqtt_client import MqttClient
from dataframe_handler import CraneDataHandler
from influxdb_writer import InfluxDbWriter

async def main():
    mqtt_client = MqttClient()
    mqtt_client.connect()

    data_frame = CraneDataHandler()
    influx_db_writer = InfluxDbWriter()

    while True:
        if mqtt_client.msg_received :
            if mqtt_client.msg != None :
                data_frame.parse_data(mqtt_client.msg.payload)
                influx_db_writer.write_crane_datas(data_frame,mqtt_client.msg.topic)
                # 插入数据后将标志位置0
                mqtt_client.msg_received = False

if __name__ == "__main__":
    asyncio.run(main())
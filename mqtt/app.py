import asyncio

from mqtt_client import MqttClient
from dataframe_handler import CraneDataHandler
from influxdb_writer import InfluxDbWriter

async def main():
    mqtt_client = MqttClient()
    mqtt_client.connect()

    data_frame = CraneDataHandler()
    influx_db_writer = InfluxDbWriter('Crane_his')

    while True:
        if mqtt_client.msg != None:
            data_frame.parse_data(mqtt_client.msg.payload)
            influx_db_writer.write_crane_datas(data_frame)

if __name__ == "__main__":
    asyncio.run(main())
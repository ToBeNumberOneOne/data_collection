import asyncio

from mqtt_client import MqttClient
from dataframe_handler import CraneDataHandler
from influxdb_writer import InfluxDbWriter

async def main():
    # 创建一个 asyncio 队列来存储MQTT消息
    message_queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    # 实例化 MQTT 客户端，并传递消息队列和事件循环
    mqtt_client = MqttClient(message_queue, loop)
    mqtt_client.connect()

    data_frame = CraneDataHandler()
    influx_db_writer = InfluxDbWriter()

    while True:
        # 异步地从队列中获取消息
        msg = await message_queue.get()
        if msg is not None:
            # 解析数据
            data_frame.parse_data(msg.payload)
            # 异步写入数据库
            await influx_db_writer.write_crane_datas_async(data_frame, msg.topic)
        message_queue.task_done()

if __name__ == "__main__":
    asyncio.run(main())

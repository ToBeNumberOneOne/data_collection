import asyncio
import paho.mqtt.client as mqtt

from CraneData import CraneDataHandler

data_frame = CraneDataHandler()

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Asc16")

# Callback when a message is received
def on_message(client, userdata, msg):
    # 解析数据
    data_frame.parse_data(msg.payload)

    print(data_frame.data_to_json())

async def main():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    client.loop_start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

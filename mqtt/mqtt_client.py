import asyncio
import paho.mqtt.client as mqtt
import struct

from CraneData import CraneData

data_frame = CraneData()

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("Asc16")

# Callback when a message is received
def on_message(client, userdata, msg):
    # 解析数据
    parsed_data =  parse_data(msg.payload)
    print(f"Receive data : {parsed_data}")

    # print(f"Topic: {msg.topic}, Message: {list_data}")

def parse_data(raw_data):
    data = {}
    word1_low = struct.unpack("b",raw_data[0:1])[0]
    word1_high = struct.unpack("b",raw_data[1:2])[0]

    data_frame.lock_state = (word1_low >> 0) & 1
    #data["lock_state"] = (word1_low >> 0) & 1
    data["unlock_state"] = (word1_low >> 1) & 1
    data["landed_state"] = (word1_low >> 2) & 1
    data["20ft"] = (word1_low >> 3) & 1
    data["40ft"] = (word1_low >> 4) & 1
    data["45ft"] = (word1_low >> 5) & 1
    data["singleMode"] = (word1_low >> 6) & 1
    data["twinMode"] = (word1_low >> 7) & 1

    data["trolleyLimit"] = (word1_high >> 0) & 1  
    data["hoistLimit"] = (word1_high >> 1) & 1 
    data["flipperSlDown"] = (word1_high >> 3) & 1
    data["flipperLlDown"] = (word1_high >> 3) & 1
    data["flipperLrDown"] = (word1_high >> 4) & 1
    data["flipperSrDown"] = (word1_high >> 5) & 1
    data["test_delay_fb"] = (word1_high >> 6) & 1  
    
    data["trolleyPos"] = round(float(struct.unpack("i",raw_data[2:6])[0])/1000,3) 
    data["hoistPos"] = round(float(struct.unpack("i",raw_data[6:10])[0])/1000,3)
    data["loadPosX"] = round(float(struct.unpack("i",raw_data[10:14])[0])/1000,3)
    data["trolleySpeed"] = round(float(struct.unpack("h",raw_data[14:16])[0])/16384*4.0,3)
    data["hoistSpeed"] = round(float(struct.unpack("h",raw_data[16:18])[0])/16384*3.0,3)
    data["loadSpeedX"] = round(float(struct.unpack("h",raw_data[18:20])[0])/1000,3)
    data["skewAngle"] = round(float(struct.unpack("h",raw_data[20:22])[0])/1000,3)
    data["twinGap"] = struct.unpack("h",raw_data[22:24])[0]

    return data

async def main():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("10.0.1.213", 1883, 60)

    client.loop_start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

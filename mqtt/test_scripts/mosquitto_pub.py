import paho.mqtt.client as mqtt
import schedule
import time
import sys

if len(sys.argv) >= 5 and str(sys.argv[1]) == "-pub":
    # Define MQTT Broker's host and port
    broker_host = str(sys.argv[2])
    broker_port = int(sys.argv[3])
    # Define MQTT topic
    topic = str(sys.argv[4])
else:
    print("请输入Mqtt broker的ip和端口号和主题,并用'-pub' 做命令选项。")
    sys.exit(1)

# Define MQTT message
# 发送数据位16机制字符串

message = bytes.fromhex("510086f100001f5b00003500000000000000a700000000000000000000000000")

# Define MQTT Client connection callback function
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker with result code {rc}")

# Define MQTT Client publish function
def publish_message(client):
    client.publish(topic, message)
    print(f"Published message: {message}")

# Create MQTT Client
client = mqtt.Client()
client.on_connect = on_connect

# Connect to MQTT Broker
client.connect(broker_host, broker_port)

# Start MQTT Client loop
client.loop_start()

# Schedule message publishing every 1 seconds
schedule.every(0.1).seconds.do(publish_message, client)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(0.001)
    
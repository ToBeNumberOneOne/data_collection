import paho.mqtt.client as mqtt
import schedule
import time

# Define MQTT Broker's host and port
broker_host = "localhost"
broker_port = 1883

# Define MQTT Client ID
#client_id = "test_client"

# Define MQTT topic
topic = "Asc16"

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
schedule.every(1).seconds.do(publish_message, client)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
    
# mqtt_client.py
import asyncio
import paho.mqtt.client as mqtt
from config import MQTT_BROKER_IP, MQTT_BROKER_PORT, MQTT_TOPICS

class MqttClient:
    def __init__(self, message_queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        self.broker_ip = MQTT_BROKER_IP
        self.broker_port = MQTT_BROKER_PORT
        self.topics = MQTT_TOPICS
        self.client = mqtt.Client()
        self.message_queue = message_queue
        self.loop = loop

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.broker_ip, self.broker_port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        for topic in self.topics:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        # 将消息放入 asyncio 队列中
        asyncio.run_coroutine_threadsafe(self.message_queue.put(msg), self.loop)
